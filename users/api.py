from typing import List, Optional

from ninja import NinjaAPI, Schema
from ninja.files import UploadedFile

from .models import Track
from .schema import NotFoundSchema, TrackSchema

api = NinjaAPI()


class HelloSchema(Schema):
    name: str = "world"


@api.post("hello/")
def hello(request, data: HelloSchema):
    return f"Hello {data.name}"


@api.get("math/{a}and{b}")
def math(request, a: int, b: int):
    return {"add": a + b, "multiply": a * b}


@api.get("tracks/", response=List[TrackSchema])
def get_tracks(request, title: Optional[str]=None):
    if title:
        return Track.objects.filter(title__contains=title)
    return Track.objects.all()


@api.get("tracks/{track_id}", response={200: TrackSchema, 404: NotFoundSchema})
def get_track(request, track_id: int):
    try:
        track = Track.objects.get(pk=track_id)
        return 200, track
    except Track.DoesNotExist:
        return 404, {"message": "Track does not exist"}


@api.post("tracks/", response={201: TrackSchema})
def post_track(request, track: TrackSchema):
    track = Track.objects.create(**track.dict())
    return track


@api.put("tracks/{track_id}", response={200: TrackSchema, 404: NotFoundSchema})
def update_track(request, track_id: int, data: TrackSchema):
    try:
        track = Track.objects.get(pk=track_id)
        for attribute, value in data.dict().items():
            setattr(track, attribute, value)
            track.save()
        return 200, track
    except Track.DoesNotExist:
        return 404, {"message": "Track does not exist"}


@api.delete("tracks/{track_id}", response={204: None, 404: NotFoundSchema})
def delete_track(request, track_id: int):
    try:
        track = Track.objects.get(pk=track_id)
        track.delete()
        return 204, None
    except Track.DoesNotExist:
        return 404, {"message": "Track does not exist"}


@api.post("/upload")
def upload(request, file: UploadedFile):
    data = file.read().decode()
    return {"name": file.name}
