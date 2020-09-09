from django.test import TestCase
from .models import Friend
from .models import Profile
from django.contrib.auth import get_user_model

User = get_user_model()

tiff = User.objects.get(username = 'Tiffany')
mark = User.objects.get(username = 'Mark')
ollie =User.objects.get(username = 'Fuck')

# tiffProfile = Profile(user = tiff, bio = 'NY')
# markProfile = Profile(user = mark, bio = 'CA')
# ollieProfile = Profile(user = ollie, bio = 'WI')

# tiffProfile.save()
# markProfile.save()
# ollieProfile.save()

# tiffFr = Friend(current_user=tiff)
# markFr = Friend(current_user=mark)
# ollieFr = Friend(current_user=ollie)

# tiffFr.save()
# markFr.save()
# ollieFr.save()

tiffFr = Friend.objects.get(current_user = tiff)
markFr = Friend.objects.get(current_user = mark)
ollieFr = Friend.objects.get(current_user = ollie)

tiffFr.make_friend(tiff, mark)
tiffFr.make_friend(tiff, ollie)
markFr.make_friend(mark, tiff)

tiffFr.save()
print(tiffFr.users.all())
print(markFr.users.all())
print(ollieFr.users.all())