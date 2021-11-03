"""Custom Mixins."""


class ContextPageMixin:
    """Custom Mixin for title and subtitle of a page."""

    def get_context_data(self, **kwargs):
        """Mixin to get intialize title and sub_title to a webpage.

        Args:
          **kwargs: Additional keyword arguments

        Returns:
          The super context with title and sub_title.
        """
        context = super().get_context_data(**kwargs)

        context["title"] = self.title
        context["sub_title"] = self.sub_title

        return context
