# :globe_with_meridians: network_

_network_ is a social network application (like twitter but with less arguing) using Python, JavaScript, HTML, and CSS.

__tl;dr:__
- Python! JavaScript! ORMs! API calls! S3 Buckets!

- see the finished project [here](https://web50network.herokuapp.com/) (it'll take a few seconds to get going as it is on a hobby server)

- favourite code snippet:
```JavaScript
  // Semi-transparent navbar onscroll
  var mainNav = document.getElementById('mainnav');
        window.onscroll = function () { 
            if (document.body.scrollTop >= 100 || document.documentElement.scrollTop >= 100) {
                mainNav.classList.add("navbar-border-transparent");
                mainNav.classList.remove("navbar-border-solid");
            } 
            else {
                mainNav.classList.add("navbar-border-solid");
                mainNav.classList.remove("navbar-border-transparent");
            }
        };
```
- what it looks like:

![network screenshot](https://s3.eu-west-2.amazonaws.com/media.jh-portfolio/media/project_images/network-1.png)

_network_ was completed for [CS50’s Web Programming with Python and JavaScript](https://online-learning.harvard.edu/course/cs50s-web-programming-python-and-javascript) course, and combines some good ol' data modelling with UI features. It incorporates extra-responsive social posts, likes and follows carried out with calls to fetch with JavaScript.

This project was a great one for thinking about how best to deliver a response to a user on larger applications. Django templates work excellently for authentication and page views but sometimes an immediate response or a nice little animation is much more pleasing than a full page reload. 

I went for a little bit of extra credit on this one by building in image upload capabilities for users. I thought this would be a fun little addition, displaying a placeholder with the first letter of a username before an image is added and it all went quite swimmingly in development. When it came to deploying on the web, things got a little bit more headachy. Still, it did give me an opportunity to look at AWS and S3 buckets which will undoubtedly come in handy for future projects.
