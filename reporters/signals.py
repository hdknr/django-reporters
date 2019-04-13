from django.dispatch import dispatcher
SignalArgs = ['message', 'fullpath']


report_created = dispatcher.Signal(providing_args=SignalArgs)
