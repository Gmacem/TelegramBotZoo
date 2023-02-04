from telegram.ext import CallbackContext, ExtBot, Application


class EnCollectorContext(CallbackContext[ExtBot, dict, dict, dict]):
    @classmethod
    def from_update(
        cls,
        update: object,
        application: "Application",
    ) -> "EnCollectorContext":
        if isinstance(update, EnCollectorContext):
            return cls(application=application, user_id=update.user_id)
        return super().from_update(update, application)
