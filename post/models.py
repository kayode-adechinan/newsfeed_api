from django.db import models
from django.contrib.auth.models import User
# Create your models here.

from PIL import Image
from django.conf import settings
import os
import uuid

def scramble_uploaded_filename(instance, filename):
    """
    Scramble / uglify the filename of the uploaded file, but keep the files extension (e.g., .jpg or .png)
    :param instance:
    :param filename:
    :return:
    """
    extension = filename.split(".")[-1]
    return "{}.{}".format(uuid.uuid4(), extension)


def create_thumbnail(input_image, thumbnail_size=(256, 256)):
    """
    Create a thumbnail of an existing image
    :param input_image:
    :param thumbnail_size:
    :return:
    """
    # make sure an image has been set
    if not input_image or input_image == "":
        return

    # open image
    image = Image.open(input_image)

    # use PILs thumbnail method; use anti aliasing to make the scaled picture look good
    image.thumbnail(thumbnail_size, Image.ANTIALIAS)

    # parse the filename and scramble it
    filename = scramble_uploaded_filename(None, os.path.basename(input_image.name))
    arrdata = filename.split(".")
    # extension is in the last element, pop it
    extension = arrdata.pop()
    basename = "".join(arrdata)
    # add _thumb to the filename
    new_filename = basename + "_thumb." + extension

    # save the image in MEDIA_ROOT and return the filename
    image.save(os.path.join(settings.MEDIA_ROOT, new_filename))

    return new_filename




class Post(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=255)
    status = models.CharField(null=True, max_length=255)
    content = models.TextField()
    rating = models.IntegerField(null=True)
    like = models.IntegerField(null=True)

    video = models.FileField("Uploaded video", upload_to=scramble_uploaded_filename, null=True)
    #video_thumbnail = models.ImageField("Thumbnail of uploaded video", blank=True)

    picture = models.ImageField("Uploaded image", upload_to=scramble_uploaded_filename, null=True)
    picture_thumbnail = models.ImageField("Thumbnail of uploaded image", blank=True)

    #def __str__(self):
        #return self.title

    class Meta:
        ordering = ['-like']

    def save(self, force_insert=False, force_update=False, using=None, update_fields=None):
        """
        On save, generate a new thumbnail
        :param force_insert:
        :param force_update:
        :param using:
        :param update_fields:
        :return:
        """
        # generate and set thumbnail or none
        self.picture_thumbnail = create_thumbnail(self.picture)

        # Check if a pk has been set, meaning that we are not creating a new image, but updateing an existing one
        # if self.pk:
        #    force_update = True

        # force update as we just changed something
        super(Post, self).save(force_update=force_update)






class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)

    avatar = models.ImageField("Uploaded image", upload_to=scramble_uploaded_filename, null=True)
    avatar_thumbnail = models.ImageField("Thumbnail of uploaded image", blank=True)

    def save(self, force_insert=False, force_update=False, using=None, update_fields=None):
        """
        On save, generate a new thumbnail
        :param force_insert:
        :param force_update:
        :param using:
        :param update_fields:
        :return:
        """
        # generate and set thumbnail or none
        self.avatar_thumbnail = create_thumbnail(self.avatar)

        # Check if a pk has been set, meaning that we are not creating a new image, but updateing an existing one
        # if self.pk:
        #    force_update = True

        # force update as we just changed something
        super(Profile, self).save(force_update=force_update)


    def __str__(self):

        return  self.avatar.url




