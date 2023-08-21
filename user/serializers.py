from rest_framework import serializers
from .models import CustomUser, Team, Task, TeamMember, TaskAssignment

class CustomUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ['userid', 'email', 'user_name' 'role', 'password']
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        user = CustomUser.objects.create(
            email=validated_data['email'],
            role=validated_data['role'],
            user_name=validated_data.get('user_name', '')
        )
        user.set_password(validated_data['password'])
        user.save()
        return user

    def update(self, instance, validated_data):
        instance.email = validated_data.get('email', instance.email)
        instance.user_name = validated_data.get('user_name', instance.user_name)
        instance.role = validated_data.get('role', instance.role)
        password = validated_data.get('password', None)
        if password:
            instance.set_password(password)
        instance.save()
        return instance

class TeamSerializer(serializers.ModelSerializer):
    team_members = serializers.SerializerMethodField(read_only=True)
    team_leader = CustomUserSerializer(read_only=True)

    class Meta:
        model = Team
        fields = ['teamid', 'name', 'team_leader', 'team_members']

    def get_team_members(self, object):
        team_members = TeamMember.objects.filter(team=object.teamid)
        member_user_ids = [member.user.userid for member in team_members]
        members_data = CustomUser.objects.filter(userid__in=member_user_ids)
        return CustomUserSerializer(members_data, many=True).data

    def validate_leader_id(self, value):
        try:
            leader = CustomUser.objects.get(firstname=value)
        except CustomUser.DoesNotExist:
            raise serializers.ValidationError("User doesn't exist")

        if leader.role != 'teamLead':
            raise serializers.ValidationError("User is not a Team leader")

        return leader

class TaskSerializer(serializers.ModelSerializer):
    class Meta:
        model = Task
        fields = ['taskid', 'name', 'team', 'status']
