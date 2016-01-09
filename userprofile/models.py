from django.db import models
from django.contrib.auth.models import User
from django.core.cache import cache
from helper.model import to_dict, get_deep_attr

# Create your models here.

class UserProfile(models.Model):

    def __str__(self):
        return self.user.username

    user = models.OneToOneField(User, related_name="profile")
    avatar = models.ImageField(upload_to="/userprofile/avatar/",default="/userprofile/avatar/default.jpg")
    # user contains: username, first_name, last_name, email, groups, use_permissions, etc

    phone_number = models.CharField(max_length=20, default="phone")

    GENDER_CHOICES = [('M', 'Male'),('F', 'Female')]
    gender = models.CharField(max_length=1, choices=GENDER_CHOICES,default='M')

    date_of_birth = models.DateField(auto_now=True)
    age = models.IntegerField(default=18)

    language = models.CharField(max_length=10,default="Martian")
    school = models.CharField(max_length=20,default="Community College")  # todo: make list of choice
    career = models.CharField(max_length=20,default="Malong")  # todo: make list of choice

    about_me = models.TextField(default="Something about myself...")

    city = models.CharField(max_length=20,default="Single City")  # todo: make list of choice
    proximity = models.IntegerField(verbose_name="Proximity (km)", default=1) # unit in km

    follower = models.ManyToManyField('self', null=True, blank=True, symmetrical=False) # one way relationship
    blocked = models.ManyToManyField('self', related_name="blocked", null=True, blank=True) # two way relationship
    recommendations = models.ManyToManyField('self', related_name='recommendation', null=True, blank=True) # two way relationship

    stranger_fields=['user__username',
                     'about_me']

    full_fields=['user__username',
                 'user__first_name',
                 'user__last_name',
                 'user__email',
                 'phone_number',
                 'gender',
                 'date_of_birth',
                 'age',
                 'language',
                 'school',
                 'career',
                 'about_me',
                 'city',
                 'proximity']

    follower_fields=['user__username',
                     'gender',
                     'school',
                     'career',
                     'about_me']

    blocked_fields=['user']


    def get_userprofile_info(self, by_userprofile):
        """
        get userprofile information by a userprofile, information provided will be based on relationship
        and how user set information will be accessed
        :param by_userprofile: userprofile requsted by
        :return: dictionary package
        """

        retVal=dict()

        if by_userprofile==self:
            # print "return full access"
            for item in self.full_fields:
                retVal[item]=get_deep_attr(self, item)

        elif self in by_userprofile.follower.all():  # if target_profile is one of my follower
            # print "return follower access"
            for item in by_userprofile.follower_fields:
                retVal[item]=get_deep_attr(self, item)

        elif by_userprofile in self.blocked.all():
            # print "return block access"
            for item in self.blocked_fields:
                retVal[item]=get_deep_attr(self, item)

        else:
            # print "stranger access"
            for item in self.stranger_fields:
                retVal[item]=get_deep_attr(self, item)

        return retVal

    def change_userprofile_info(self, field, new_value):
        if field in ['username', 'first_name', 'last_name', 'email']:
            setattr(self.user,field,new_value)
        else:
            setattr(self,field,new_value)
        self.save()

    def get_blocked(self):
        """
        :return:  UserProfile blocked as query set
        """
        blocked_list = self.blocked.all().values_list('user__username', flat=True)

        return blocked_list

    def get_follower(self):
        """
        :return:  UserProfile followers as query set
        """
        follower_list = self.follower.all().values_list('user__username', flat=True)

        return follower_list

    def rs_follow(self, target_userprofile):
        """
        follow target userprofile
        :param target_userprofile:
        :return:
        """
        try:
            self.blocked.remove(target_userprofile)
        except:
            pass

        target_userprofile.follower.add(self)

        target_userprofile.save()
        self.save()

    def rs_block(self, target_userprofile):
        """
        block target user profile
        :param target_userprofile:
        :return:
        """
        self.blocked.add(target_userprofile)
        try:
            target_userprofile.follower.remove(self)
        except:
            pass

        target_userprofile.save()
        self.save()

    def rs_reset(self, target_userprofile):
        """
        reset relationship to stranger
        :param target_userprofile:
        :return:
        """

        try:
            target_userprofile.follower.remove(self)
        except:
            pass

        try:
            self.blocked.remove(target_userprofile)
        except:
            pass

        target_userprofile.save()
        self.save()


# algorithm should use these parameters to match other users
    @staticmethod
    def get_match_parameter(user):
        match_parameter=dict()

        match_parameter["gender"]=getattr(user,'gender')
        match_parameter["DOB"]= getattr(user,'date_of_birth')
        match_parameter["proximity"]=getattr(user,'proximity')

        return match_parameter


