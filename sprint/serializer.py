from rest_framework import serializers
from .utils import InsertionError
from .models import Sprint, Parameter, Votes, ShowResult,SpecialMentions


class SprintSerializer(serializers.Serializer):
    """
   Serializer for Converting Python object for  Parameter Table
    """
    id = serializers.IntegerField(required=False)
    sprint_name = serializers.CharField(required=False)
    start_date = serializers.DateField(required=False)
    end_date = serializers.DateField(required=False)
    is_active = serializers.BooleanField(default=True, required=False)
    show_result = serializers.BooleanField(default=False, required=False)

    def create(self, validate_data):
        """
        for creating the sprint
        :param validate_data:  validate the api data
        :return: sprint
        """
        sprint = Sprint.objects.filter(is_active=True)
        if not sprint:
            sprint = Sprint.objects.create(
                sprint_name=validate_data.get("sprint_name"),
                start_date=validate_data.get("start_date"),
                end_date=validate_data.get("end_date"),
            )
            return sprint
        else:
            raise InsertionError("One Sprint is already Active")

    def update(self, instance, validated_data):
        """
        Update and return an existing `Snippet` instance, given the validated data.
        """
        instance.id = validated_data.get('id', instance.id)
        instance.sprint_name = validated_data.get('sprint_name', instance.sprint_name)
        instance.start_date = validated_data.get('start_date', instance.start_date)
        instance.end_date = validated_data.get('end_date', instance.end_date)
        instance.is_active = validated_data.get('is_active', instance.is_active)
        instance.show_result = validated_data.get('show_result', instance.show_result)

        instance.save()
        return instance


class ParamSerializer(serializers.Serializer):
    """
    Serializer for Converting Python object for  Parameter Table
    """
    id = serializers.IntegerField(required=False)
    parameter_name = serializers.CharField(required=True)

    def create(self, validate_data):
        parameter = Parameter.objects.create(
            parameter_name=validate_data.get("parameter_name")
        )
        return parameter

    def update(self, instance, validated_data):
        instance.parameter_name = validated_data.get('parameter_name', instance.parameter_name)
        instance.save()
        return instance


class VoteSerializer(serializers.ModelSerializer):
    """
    Serializer is user to converting the python object for the Vote
    """

    class Meta:
        model = Votes
        fields = "__all__"

    def create(self, validated_data):
        """
        for the votes operations
        :param validated_data: validating the api data
        :return: vote
        """
        vote = Votes.objects.create(
            sprint_id=validated_data.get("sprint_id"),
            parameter_id=validated_data.get("parameter_id"),
            vote_by=validated_data.get("vote_by"),
            vote_to=validated_data.get("vote_to"),
        )

        return vote


class ShowResultSerializer(serializers.Serializer):
    """
    Serializer is user to converting the python object for the Vote
    """

    sprint_id = serializers.IntegerField(required=False)
    show = serializers.BooleanField(default=False)

    def create(self, validated_data):
        """
        for the votes operations
        :param validated_data: validating the api data
        :return: vote
        """
        showResult = ShowResult.objects.create(
            sprint_id=validated_data.get("sprint_id"),
            show=validated_data.get("show"),
        )

        return showResult

    def update(self, instance, validated_data):
        instance.id = validated_data.get('id', instance.id)
        instance.sprint_id = validated_data.get('sprint_id', instance.sprint_id)
        instance.show = validated_data.get('show', instance.show)
        instance.save()
        return instance


class SpecialMentionSerializer(serializers.Serializer):
    """
    Serializer is user to converting the python object for the Vote
    """

    sprint_id = serializers.IntegerField(required=True)
    special_mentions = serializers.CharField(max_length=200, required=False)
    vote_by = serializers.IntegerField()

    def create(self, validated_data):
        """
        for the votes operations
        :param validated_data: validating the api data
        :return: vote
        """
        specialMention = SpecialMentions.objects.create(
            sprint_id=validated_data.get("sprint_id"),
            special_mentions=validated_data.get("special_mentions"),
            vote_by=validated_data.get("vote_by")
        )

        return specialMention

    def update(self, instance, validated_data):
        instance.id = validated_data.get('id', instance.id)
        instance.sprint_id = validated_data.get('sprint_id', instance.sprint_id)
        instance.special_mentions = validated_data.get('special_mentions', instance.special_metions)
        instance.vote_by = validated_data.get('vote_by', instance.vote_by)
        instance.save()
        return instance
