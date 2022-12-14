import json
import logging
from collections import Counter
from itertools import count
from django.db import transaction
from .models import Sprint, Parameter, Votes, ShowResult, Game, SpecialMentions
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from .serializer import SprintSerializer, ParamSerializer, VoteSerializer, ShowResultSerializer, \
    SpecialMentionSerializer
from rest_framework.exceptions import ValidationError
from .utils import InsertionError, AlreadyPresentException, verify_token, is_superuser
from user.models import User

logging.basicConfig(filename="sprint.log", filemode="w")


class SprintC(APIView):

    @verify_token
    @is_superuser
    def post(self, request):
        """
        For Adding sprint Cycle
        :param request:
        :return:Response
        """
        try:
            serializer = SprintSerializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            serializer.save()
            # showSerializer = ShowResultSerializer(data={"sprint_id": sprint.id, "show": False})
            #
            # showSerializer.is_valid()
            # showSerializer.save()

            return Response(
                {
                    "message": "Sprint Added Successfully",
                    "data": serializer.data
                }, status=status.HTTP_201_CREATED)


        except InsertionError as e:
            return Response(
                {
                    "message": "Error Occurred",
                    "error": str(e)
                }, status=status.HTTP_400_BAD_REQUEST
            )
        except Exception as e:
            return Response(
                {"message": "Error Occurred",
                 "error": str(e)
                 }, status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

    @verify_token
    @is_superuser
    def put(self, request, id):
        """
        For Updating the Sprint Cycle
        :param request:
        :return:
        """
        try:

            if not Sprint.objects.filter(id=id):
                return Response(
                    {
                        "message": "Sprint Does Not Exist"
                    }, status=status.HTTP_404_NOT_FOUND
                )

            current_sprint = Sprint.objects.get(id=id)
            exc = Sprint.objects.exclude(sprint_name=current_sprint.sprint_name)

            for sprints in exc:
                if sprints.is_active == True:
                    return Response(
                        {
                            "message": "Updation failed",
                            "error": "A Sprint is Already Active Please Disable It First"
                        }, status=status.HTTP_400_BAD_REQUEST
                    )

            sprint = Sprint.objects.get(id=id)
            serializer = SprintSerializer(sprint, data=request.data)
            serializer.is_valid(raise_exception=True)
            serializer.save()

            return Response(
                {
                    "message": "Sprint updated successfully",
                    "data": serializer.data
                }, status=status.HTTP_200_OK
            )

        except ValidationError:
            logging.error("Validation failed")
            return Response(
                {
                    "message": "Sprint not updated"
                },
                status=status.HTTP_400_BAD_REQUEST)

        except Exception as e:
            return Response(
                {
                    "message": "Error Occurred",
                    "error": str(e)
                }, status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )

    @verify_token
    def get(self, request):
        """
             this method is created for retrieve data
             :param request: format of the request
             :return: Response
        """
        try:

            all_sprint = Sprint.objects.all()
            serializer = SprintSerializer(all_sprint, many=True)
            active_sprint = Sprint.objects.filter(is_active=True)
            aserializer = SprintSerializer(active_sprint, many=True)

            if active_sprint:
                return Response(
                    {
                        "message": " Sprint is active:",
                        "data": serializer.data,
                        "is_active": aserializer.data
                    }, status=status.HTTP_200_OK
                )
            return Response(
                {
                    "message": "Sprint is not active:",
                    "data": serializer.data,
                }, status=status.HTTP_200_OK
            )

        except Exception as e:
            return Response(
                {
                    "message": "Error Occurred",
                    "error": str(e)
                }, status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

    @verify_token
    @is_superuser
    def delete(self, request, id):
        """
        This method is created for delete the existing data
        :param request: format of the request
        :param id: sprint id
        :return: Response
        """
        try:

            if not Sprint.objects.filter(id=id):
                return Response(
                    {
                        "message": "Sprint Does Not Exist"
                    }, status=status.HTTP_404_NOT_FOUND
                )
            sprint = Sprint.objects.get(id=id)
            sprint.delete()
            return Response(
                {
                    "message": "Sprint deleted successfully"
                },
                status=status.HTTP_200_OK)

        except ValidationError:
            logging.error("Validation failed")
            return Response(
                {
                    "message": "Sprint not deleted"
                },
                status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            logging.error(e)
            return Response(
                {
                    "message": "Exception Occurred",
                },
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )


class VoteParameter(APIView):
    @verify_token
    @is_superuser
    def post(self, request):
        """
        For Adding Parameter for voting
        :param request:
        :return: Response
        """
        try:

            serializer = ParamSerializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            serializer.save()
            return Response({
                "message": "Parameter Added Successful",
                "data": serializer.data
            },
                status=status.HTTP_201_CREATED)

        except ValidationError:
            logging.error("Validation failed")
            return Response(
                {
                    "message": "validation failed"
                },
                status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:

            return Response({
                "message": "Error Occurred",
                "error": str(e)
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    @verify_token
    def get(self, request):
        """
        For Getting the list of all the parameter
        :param request:
        :return:
        """
        try:
            parameters = Parameter.objects.all()
            serializer = ParamSerializer(parameters, many=True)
            return Response(
                {
                    "message": "Here your Parameters",
                    "data": serializer.data
                }, status=status.HTTP_200_OK
            )
        except ValidationError:
            logging.error("Validation failed")
            return Response(
                {
                    "message": "validation failed"
                },
                status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            logging.error(e)
            return Response(
                {
                    "message": "Error Occurred",
                    "error": str(e),
                },
                status=status.HTTP_400_BAD_REQUEST)

    @verify_token
    @is_superuser
    def put(self, request, id):
        """
        USed for updating existing Parameter
        :param request:
        :param paramID: id of parameter you want to update
        :return:
        """
        try:
            if not Parameter.objects.filter(id=id):
                return Response(
                    {
                        "message": "Parameter Does Not Exist"
                    }, status=status.HTTP_404_NOT_FOUND
                )
            parameter = Parameter.objects.get(id=id)
            serializer = ParamSerializer(parameter, data=request.data)
            serializer.is_valid(raise_exception=True)
            serializer.save()
            return Response(
                {
                    "message": "Parameter updation  successful",
                    "data": serializer.data
                }, status=status.HTTP_200_OK
            )

        except ValidationError:
            return Response(
                {
                    "message": "Validation error"
                }, status=status.HTTP_400_BAD_REQUEST
            )
        except Exception as e:
            logging.error(e)
            return Response(
                {
                    "message": "Error Occurred",
                    "error": str(e)
                }, status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

    @verify_token
    @is_superuser
    def delete(self, request, id):
        """
        For Delete The Existing Parameter
        :param id:id of the parameter you want to delete
        :return: Response
        """
        try:
            if not Parameter.objects.filter(id=id):
                return Response(
                    {
                        "message": "Parameter Does Not Exist"
                    }, status=status.HTTP_404_NOT_FOUND
                )
            parameter = Parameter.objects.get(id=id)
            parameter.delete()
            return Response(
                {
                    "message": "Deletion Successful"
                }, status=status.HTTP_200_OK
            )

        except ValidationError:
            return Response(
                {
                    "message": "Validation error"
                }, status=status.HTTP_400_BAD_REQUEST
            )
        except Exception as e:
            logging.error("Exception Occurred")
            return Response(
                {
                    "message": "Exception Occurred",
                    "error": str(e)
                }, status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )


class Voting(APIView):
    @transaction.atomic
    @verify_token
    def post(self, request, id):
        try:
            parameter_list = request.data.get("parameter_list")
            if not Sprint.objects.filter(id=id, is_active=True):
                return Response(
                    {
                        "message": "this Sprint is not active"
                    }, status=status.HTTP_400_BAD_REQUEST
                )
            with transaction.atomic():
                for parameter in parameter_list:
                    parameter.update({"sprint_id": id})
                    parameter.update({"vote_by": request.data.get("user_id")})

                    vote = Votes.objects.filter(vote_by=request.data.get("user_id"),
                                                parameter_id=parameter.get("parameter_id"),
                                                sprint_id=id)

                    if parameter.get("vote_by") == parameter.get("vote_to"):
                        raise InsertionError


                    elif vote:
                        raise AlreadyPresentException

                    serializer = VoteSerializer(data=parameter)
                    serializer.is_valid(raise_exception=True)
                    serializer.save()

            return Response(
                {
                    "message": "Voting Successful"
                }, status=status.HTTP_201_CREATED
            )
        except InsertionError:
            return Response(
                {
                    "message": "You cannot Vote for yourself",
                    "data": parameter
                }, status=status.HTTP_400_BAD_REQUEST
            )

        except AlreadyPresentException:
            return Response(
                {
                    "message": "Parameter addition Unsuccessful-already voted on this parameter",
                    "data": parameter
                }, status=status.HTTP_400_BAD_REQUEST
            )
        except Exception as e:
            logging.error(e)

            return Response(
                {
                    "message": "Exception Occurred",
                    "error": str(e)
                }, status=status.HTTP_400_BAD_REQUEST
            )

    @verify_token
    def get(self, request, id):
        """
        For getting the details of vote done by a user
        :param request:
        :param id: User id of how is login
        :return: Response
        """
        try:

            votes = Votes.objects.filter(vote_by=request.data.get("user_id"), sprint_id=id)
            serializer = VoteSerializer(votes, many=True)
            vote_list = list()
            if serializer.data:
                for vote in serializer.data:
                    vote_list.append({"parameter_id": vote.get("parameter_id"), "vote_to": vote.get("vote_to")})
                vote_data = {
                    "Vote_by": request.data.get("user_id"),
                    "sprint_id": id,
                    "vote_details": vote_list
                }
                return Response(
                    {
                        "message": "Here is your data",
                        "data": vote_data
                    }, status=status.HTTP_200_OK
                )
            return Response(
                {
                    "message": "He has Not vote for any parameter",

                }, status=status.HTTP_404_NOT_FOUND
            )
        except ValidationError:
            return Response(
                {
                    "message": "validation error"
                }, status=status.HTTP_400_BAD_REQUEST
            )
        except Exception as e:
            logging.error(e)
            return Response(
                {
                    "message": "Error Occurred",
                    "error": str(e)
                }, status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

    @verify_token
    def put(self, request, id):
        """
        For updating the existing votes
        :param request:
        :param id: Id of the sprint
        :return: Response
        """
        try:

            parameter_list = request.data.get("parameter_list")
            if not Sprint.objects.filter(id=id, is_active=True):
                return Response(
                    {
                        "message": "this Sprint is not active"
                    }, status=status.HTTP_400_BAD_REQUEST
                )
            for parameter in parameter_list:
                parameter.update({"sprint_id": id})
                parameter.update({"vote_by": request.data.get("user_id")})
                votes_obj = Votes.objects.filter(
                    vote_by=parameter.get("vote_by"),
                    parameter_id=parameter.get("parameter_id"),
                    sprint_id=parameter.get("sprint_id")
                ).first()
                if parameter.get("vote_by") == parameter.get("vote_to"):
                    return Response(
                        {
                            "Message": "You Can not update your self parameter",
                        },
                        status=status.HTTP_400_BAD_REQUEST
                    )
                else:
                    if votes_obj is None:
                        serializer = VoteSerializer(instance=votes_obj, data=parameter)
                        serializer.is_valid(raise_exception=True)
                        serializer.save()
                    else:
                        votes_obj.delete()
                        serializer = VoteSerializer(data=parameter)
                        serializer.is_valid(raise_exception=True)
                        serializer.save()
            return Response(
                {
                    "message": "Your vote is updated",

                }, status=status.HTTP_200_OK
            )
        except ValidationError as e:
            return Response(
                {
                    "message": "Validation error!!!!!!!!",
                    "error": str(e)
                }, status=status.HTTP_400_BAD_REQUEST
            )
        except Exception as e:
            return Response(
                {
                    "message": "Error Occurred..",
                    "error": str(e)
                }, status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )


class Result(APIView):
    """
    For Retreving the result of voting held
    """

    @verify_token
    def get(self, request, id):
        """
        For getting the result
        :param request:
        :param id: id of sprint
        :return: Response
        """
        try:
            if not Sprint.objects.filter(id=id):
                return Response(
                    {
                        "message": "Sprint Doesn't Exists"
                    }, status=status.HTTP_404_NOT_FOUND
                )
            votes = Votes.objects.filter(sprint_id=id)
            serializer = VoteSerializer(votes, many=True)
            list_of_votes = list()
            vote_details = list()
            for vote_dic in serializer.data:
                if (vote_dic["vote_to"]) != None:
                    vote_to = User.objects.get(id=vote_dic["vote_to"])
                    parameter = Parameter.objects.get(id=vote_dic.get("parameter_id"))
                    vote_by = User.objects.get(id=vote_dic.get("vote_by"))
                    vote_obj = {"vote_to": vote_to.first_name.capitalize(), "vote_by": vote_by.first_name.capitalize(),
                                "parameter_name": parameter.parameter_name}
                    vote_details.append(vote_obj)

                    list_of_votes.append(vote_to.first_name.capitalize())
            vote_count = Counter(list_of_votes)
            dataPoints = list()
            for vote in vote_count:
                voteObj = {"label": vote, "y": vote_count[vote]}
                dataPoints.append(voteObj)

            winner = max(vote_count.values())

            winner_list = [k for k, v in vote_count.items() if v == winner]

            for w in winner_list:
                vote_count.pop(w)
            if vote_count.values():
                first_runner_up = max(vote_count.values())
            first_runner_up_list = [k for k, v in vote_count.items() if v == first_runner_up]

            for w in first_runner_up_list:
                vote_count.pop(w)
            if vote_count.values():
                second_runner_up = max(vote_count.values())
            second_runner_up_list = [k for k, v in vote_count.items() if v == second_runner_up]

            return Response(
                {
                    "winner": winner_list,
                    "first_runner_up": first_runner_up_list,
                    "second_runner_up": second_runner_up_list,
                    "vote_count": dataPoints,
                    "vote_details": vote_details
                },
                status=status.HTTP_200_OK)
        except Exception as e:
            print(e)
            return Response(
                {
                    "message": "Errror Occurred",
                    "error": str(e)
                }, status=status.HTTP_400_BAD_REQUEST
            )


class SprintData(APIView):

    @verify_token
    def get(self, request):
        try:
            users = User.objects.all()
            list_of_username = list()
            for user in users:
                if request.data.get("user_id") != user.id:
                    full_name = user.first_name + " " + user.last_name

                    user_obj = {"name": full_name, "id": user.id}
                    list_of_username.append(user_obj)

            return Response(
                {
                    "message": "Got the data",
                    "data": list_of_username

                }
            )
        except Exception as e:
            return Response(
                {
                    "message": "Exception Occurred",
                    "error": str(e)
                }
            )


class ShowResultApi(APIView):

    @verify_token
    def post(self, request):
        try:
            ex = ShowResult.objects.filter(sprint_id=request.data.get("sprint_id"))

            if (len(ex) > 0):
                return Response(
                    {
                        "message": "show result data already exist"
                    }
                )
            sprint = Sprint.objects.get(id=request.data.get("sprint_id"))
            print(sprint)
            if sprint:
                sp = ShowResult.objects.create(sprint_id=sprint, show=request.data.get("show"))
                print(sp)

                return Response(
                    {
                        "message": "show result data added",
                    }, status=status.HTTP_201_CREATED
                )
            return Response(
                {
                    "message": "sprint not exist",
                }, status=status.HTTP_400_BAD_REQUEST
            )

        except Exception as e:
            return Response(
                {
                    "message": "Exception Occurred",
                    "error": str(e)
                }
            )

    @verify_token
    def put(self, request, id):
        """
        USed for updating existing Parameter
        :param request:
        :param paramID: id of parameter you want to update
        :return:
        """
        try:
            if not Sprint.objects.filter(id=id):
                return Response(
                    {
                        "message": "Sprint Does Not Exist"
                    }, status=status.HTTP_404_NOT_FOUND
                )
            sprint = ShowResult.objects.get(sprint_id=id)

            serializer = ShowResultSerializer(sprint, data=request.data)
            serializer.is_valid(raise_exception=True)
            serializer.save()
            return Response(
                {
                    "message": "Show Result updation  successful",
                    "data": serializer.data
                }, status=status.HTTP_200_OK
            )
        except Exception as e:
            return Response(
                {
                    "message": "Exception Occurred",
                    "error": str(e)
                }
            )

    @verify_token
    def get(self, request):
        """
        For Getting the list of all the parameter
        :param request:
        :return:
        """
        try:
            show = ShowResult.objects.all()
            list_of_shows = list()
            for s in show:
                sobj = {"sprint_id": s.sprint_id_id, "show": s.show, "id": s.id}
                list_of_shows.append(sobj)
            return Response(
                {
                    "message": "Here your Result",
                    "data": list_of_shows
                }, status=status.HTTP_200_OK
            )
        except ValidationError:
            logging.error("Validation failed")
            return Response(
                {
                    "message": "validation failed"
                },
                status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            logging.error(e)
            return Response(
                {
                    "message": "Error Occurred",
                    "error": str(e),
                },
                status=status.HTTP_400_BAD_REQUEST)

    @verify_token
    def delete(self, request, id):
        """
        For Delete The Existing Parameter
        :param id:id of the parameter you want to delete
        :return: Response
        """
        try:
            if not ShowResult.objects.filter(sprint_id=id):
                return Response(
                    {
                        "message": "Does Not Exist"
                    }, status=status.HTTP_404_NOT_FOUND
                )
            parameter = ShowResult.objects.get(sprint_id=id)
            parameter.delete()
            return Response(
                {
                    "message": "Deletion Successful"
                }, status=status.HTTP_200_OK
            )

        except ValidationError:
            return Response(
                {
                    "message": "Validation error"
                }, status=status.HTTP_400_BAD_REQUEST
            )
        except Exception as e:
            logging.error("Exception Occurred")
            return Response(
                {
                    "message": "Exception Occurred",
                    "error": str(e)
                }, status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )


class Gaming(APIView):
    @verify_token
    def post(self, request):
        try:
            sprint_id = request.data.get("sprint_id")
            sprint = Sprint.objects.get(id=sprint_id)

            user_id = request.data.get("user_id")
            score = request.data.get("score")
            game = Game.objects.filter(sprint_id=sprint, user_id=user_id)
            if game:
                game.delete()

            game = Game.objects.create(sprint_id=sprint, user_id=user_id, score=score)
            game.save()

            return Response(
                {
                    "message": "Score Added Successfully",

                }, status=status.HTTP_201_CREATED
            )
        except Exception as e:
            return Response(
                {
                    "message": "Exception Occurres",
                    "Error": str(e),

                }, status=status.HTTP_400_BAD_REQUEST
            )

    def get(self, request, id):
        try:
            sprint = Sprint.objects.get(id=id)
            game = Game.objects.filter(sprint_id=sprint)

            list_of_score = list()
            for g in game:
                user = User.objects.get(id=g.user_id)
                game_obj = {"username": user.first_name, "score": g.score}
                list_of_score.append(game_obj)

            return Response(
                {
                    "message": "Here your data",
                    "data": list_of_score
                }, status=status.HTTP_200_OK
            )
        except Exception as e:
            return Response(
                {
                    "message": "Exception Occurred",
                    "error": str(e)
                }
            )

    def delete(self, request):
        try:
            game = Game.objects.all()
            game.delete()
            return Response(
                {
                    "message": "Game data deleted",
                }
            )
        except Exception as e:
            return Response(
                {
                    "message": "Exception occurred",
                    "error": str(e)
                }
            )


class SpecialMention(APIView):
    @verify_token
    def post(self, request):
        try:
            print(request.data)
            vote_by = request.data.get("user_id")
            request.data.update({"vote_by": vote_by})
            sprint = Sprint.objects.get(id=request.data.get("sprint_id"))
            if (sprint):
                specialmention = SpecialMentions.objects.filter(vote_by=request.data.get("vote_by"),
                                                                sprint_id=request.data.get("sprint_id"))
                if specialmention:
                    specialmention.delete()
                if request.data.get("special_mentions").strip() != "":
                    special_mentions = SpecialMentions.objects.create(sprint_id=sprint,
                                                                      vote_by=User.objects.get(
                                                                          id=request.data.get("user_id")),
                                                                      special_mentions=request.data.get(
                                                                          "special_mentions"))
                    special_mentions.save()
                    return Response(
                        {
                            "message": "special mention added"
                        }
                    )

            return Response(
                {
                    "message": "Special mention unsuccess",

                }, status=status.HTTP_400_BAD_REQUEST
            )
        except Exception as e:
            return Response(
                {
                    "message": "Exception Occurres",
                    "Error": str(e),

                }, status=status.HTTP_400_BAD_REQUEST
            )

    @verify_token
    def get(self, request, sprint_id):
        try:
            vote_by = request.data.get("user_id")
            request.data.update({"vote_by": vote_by})
            specal_mention = SpecialMentions.objects.filter(vote_by=request.data.get("vote_by"),
                                                            sprint_id=sprint_id)

            if specal_mention:
                vote_by = User.objects.get(id=request.data.get("vote_by"))
                special_mention_dict = {"vote_by": vote_by.username,
                                        "special_mention": specal_mention[0].special_mentions,
                                        "sprint_id": sprint_id}
                return Response(
                    {
                        "message": "here is your data",
                        "data": json.dumps(special_mention_dict)

                    }, status=status.HTTP_200_OK
                )
            return Response(
                {
                    "message": "No data found"
                }, status=status.
                HTTP_400_BAD_REQUEST
            )
        except Exception as e:
            return Response(
                {
                    "message": "Exception Occurded",
                    "error": str(e)
                }, status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )


class SpecialMentionResult(APIView):
    def get(self, request, id):
        try:
            special_mention_list = SpecialMentions.objects.filter(sprint_id=id)
            list_of_special_mention = list()
            for mention in special_mention_list:
                mention_obj = {"vote_by": mention.vote_by.first_name, "special_mentions": mention.special_mentions}
                list_of_special_mention.append(mention_obj)

            return Response(
                {
                    "message": "Here is Your Data",
                    "data": list_of_special_mention
                }
            )
        except Exception as e:
            return Response(
                {
                    "message": "Exception Occurred",
                    "error": str(e)
                }
            )
