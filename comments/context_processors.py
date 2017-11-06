from .forms import ReportSuggestionForm


def report_suggestion_form(request):
    message_form = ReportSuggestionForm()
    return {'message_form': message_form}
