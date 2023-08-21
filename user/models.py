from django.db import models
from django.utils import timezone
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin


    


# Custom user model
class UserManager(BaseUserManager):
    def create_user(self,user_name,email,password,role,**extra_fields):
        if not user_name:
            raise ValueError("Username is required")
        if not email:
            raise ValueError("Email is required")
        if not role:
            raise ValueError("Role is required")
        email=self.normalize_email(email)
        user=self.model(email=email,role=role,**extra_fields)
        user.set_password(password)
        user.save(using=self.db)
        return user
    
    
    def create_superuser(self,user_name,email,password,role,**extra_fields):
        extra_fields.setdefault('is_staff',True)
        extra_fields.setdefault('is_superuser',True)
        extra_fields.setdefault('is_active',True)
        
        return self.create_user(user_name,email,password,role,**extra_fields)

class CustomUser(AbstractBaseUser, PermissionsMixin):

    ROLES = [
        ('Manager', 'Manager'),
        ('TeamLeader', 'Team Leader'),
        ('TeamMember','Team Member'),
    ]
     
    user_name = models.CharField(max_length=100, primary_key=True, unique=True)
    email = models.EmailField(unique=True)
    password = models.CharField(max_length=128)
    role=models.CharField(max_length=15, choices=ROLES, default= 'TeamMember')
    
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)

    


    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['role', 'user_name']
    
    objects = UserManager()

# Team model
class Team(models.Model):
    team_name = models.CharField(max_length=255, unique=True)
    team_leader = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='team_leads', limit_choices_to={'role':'TeamLeader'})

    class Meta:
        unique_together = ['team_name', 'team_leader']
    def __str__(self):
        return self.team_name
    
# Team member model
class TeamMember(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    team = models.ForeignKey(Team, on_delete=models.CASCADE)

    class Meta:
        unique_together = ['user', 'team']
    
    def __str__(self):
        return self.user.user_name

# Task model
class Task(models.Model):
   
    STATUSES = [
        ("CREATED",'Created'),
        ("ASSIGNED", 'Assigned'),
        ("Inprogress", 'In progress'),
        ("UnderReview",'Under Review'),
        ("Done",'Done'),
    ]
    
    taskid = models.AutoField(primary_key=True)
    name = models.CharField(max_length=255,unique=True)
    team = models.ForeignKey(Team, on_delete=models.CASCADE, related_name='tasks')
    status = models.CharField(max_length=12, choices=STATUSES, default="CREATED")
    started_at = models.DateTimeField(auto_now_add=True)
    completed_at = models.DateTimeField(null=True, blank=True)

    @property
    def is_completed(self):
        return self.status == "Done"
    
    def save(self, *args, **kwargs):
        if self.status == "Done" and not self.completed_at:
            self.completed_at = timezone.now()
        elif self.status != "Done" :
            self.completed_at = None
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name

# Task assignment model
class TaskAssignment(models.Model):
    task = models.ForeignKey(Task, on_delete=models.CASCADE)
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    
    class Meta:
    
      unique_together = ['task', 'user']

    def __str__(self):
        return self.task.name
