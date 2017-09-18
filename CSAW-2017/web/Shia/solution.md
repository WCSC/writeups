# Solution for Shia Labeouf-off!

## Things to know

This challenge is based on the python web framework, Django. Before jumping into this one, review Django and templates in Django.

## Walkthrough

### Step 1: Investigation

#### Homepage and polls

When you first pull up this challenge, you will be on the homepage, with a Shia Surprise!

Viewing the source for this page reveals nothing useful; let's move on.

When you click the "Pick ur Shia!" button, you are brought to a new page, /polls/, which has 2 links to polls. Clicking one of the two, we are brought to a new url, http://web.chal.csaw.io:5487/polls/2/, and the number in the url immediately sticks out. Trying to change the url to 3 results in an error.

		http://web.chal.csaw.io:5487/polls/3/

We are quickly greeted by a wall of error text! This may (and will) be useful later, but for now, let's move on.

#### Ad-Lib

Returning to the homepage, we can follow another link to /ad-lib/, where we are presented with a textbox with the following instructions:

> Give me an ad lib and I will Shia Labeouf it up for you!
> Where you want a noun, just put: "{{ noun }}", for a verb: "{{ verb }}", and for an adjective: "{{ adjective }}"!

I was not familiar with Django when I started this challenge; however, this stands out immediately as some kind of programming language. Googling django and {{ }} reveals that we are looking at Djangos templates. It appears we have found our vulnerability.

However, we do not have a direction for our exploit. Since the debug is on, let's go ahead and get an error on this page as well. This is easily done by inserting some weird Django template, such as:

		{{ * }}

### Step 2: Searching for our flag

#### Mrpoopy

We now have two useful error pages, one on the polls page and one on the adlib page.

When looking through django errors, it's useful to look for code on the error trace that was created by the user, not the library. You can find this code by looking for files with clearly user-generated names, or starting with ./  (Clicking on the one-line code excerpt will expand it.)

Scrolling through it, we find this:

		./ad-lib/views.py in index

		def index(request):
		global obj
		if request.method == "POST":
			data = request.POST.get('formatdata', '')
			template_data = TEMP.format(data.replace("noun", "noun|safe").replace("verb", "verb|safe").replace("adjective", "adjective|safe"))
			template = Template(template_data)
			context = RequestContext(request, {
				'noun': '<img src="https://media0.giphy.com/media/arNexgslLkqVq/200.webp#70-grid1" />',
				'verb': '<img src="https://media3.giphy.com/media/R0vQH2T9T4zza/200.webp#165-grid1" />',
				'adjective': '<img src="https://media1.giphy.com/media/TxXhUgEUWWL6/200.webp#129-grid1" />',
				'mrpoopy': obj
		})

We have found the values we were calling earlier! However, we also found an object, mrpoopy. Let's try to print this by injection again:

		{{ mrpoopy }}

We are given the following:

> <ad-lib.someclass.Woohoo instance at 0x7f9d71900680>

This is a fairly strange object, and in a convenient location, so our flag is probably hiding here. Unfortunately, we have no way to know what attributes are in the object, such as by calling the dir function in python.

#### Finding Mypoopy's attributes

Let us view our other source of knowledge, the errors in the polls page. We will do what we did before, and search for user-written code. We find, amongst other things:

		./polls/templatetags/pools_extras.py in checknum

		@register.filter(name='getme')
		def getme(value, arg):
			return getattr(value, arg)

		@register.filter(name='checknum')
		def checknum(value):
			check(value)

		@register.filter(name='listme')
		def listme(value):
			return dir(value)

		def check(value):

That listme is exactly what we need! This file is in the folder templatetags. If we google this, we find these are custom functions that act like "filters" for our templates. The following prints my_date, formatted as Y-m-d:

		{{ my_date|date:"Y-m-d" }}

The custom listme calls dir on the variable, which is exactly what we need! The getme might also be useful, so let's keep it in mind.

### Step 3: Exploit!

Let's go bck to the ad-lib page and find out what secrets mrpoopy holds. Inject the following:

		{{ mrpoopy|listme }}

We get the following:

		['Woohoo', '__doc__', '__flag__', '__module__']

Perfect! That flag value is exactly what we need! You just killed Shia Labeouf!

		{{ mrpoopy.__flag__ }}

Wait... He's not dead! Shia Surprise! (https://www.youtube.com/watch?v=o0u4M6vppCI) We got a syntax error, as variables and attributes may not begin with underscores. Fortunately, we found a function earlier that is not so limiting: getme. Let's use it here!

		{{ mrpoopy|getme:"__flag__" }}

Congratulations! You have just beat Shia Labeouf. For real this time. And you kept all your limbs!

## Flag

		flag{wow_much_t3mplate}
