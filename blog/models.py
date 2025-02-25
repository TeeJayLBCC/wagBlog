from django.db import models

# Add these: - step one
from wagtail.models import Page
from wagtail.fields import RichTextField


# add this: - step two
from wagtail.search import index

# keep the definition of BlogIndexPage model, - step two
class BlogIndexPage(Page):
    intro = RichTextField(blank=True)

    # add the get_context method: - step three
    def get_context(self, request):
        # Update context to include only published posts, ordered by reverse-chron
        context = super().get_context(request)
        blogpages = self.get_children().live().order_by('-first_published_at')
        context['blogpages'] = blogpages
        return context

    content_panels = Page.content_panels + ["intro"]

# and add the BlogPage model: - step two
class BlogPage(Page):
    date = models.DateField("Post date")
    intro = models.CharField(max_length=250)
    body = RichTextField(blank=True)

    search_fields = Page.search_fields + [
        index.SearchField('intro'),
        index.SearchField('body'),
    ]

    content_panels = Page.content_panels + ["date", "intro", "body"]

