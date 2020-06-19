
class Insert:
    def __init__(self):
        self.fields_types = ["ForeignKey", "AutoField"]

    def save_model(self, model, json_post):
        model_structure = {x.name: model._meta.get_field(
            x.name).get_internal_type() for x in model._meta.get_fields()}
        for x in model_structure:
            if model_structure[x] not in self.fields_types:
                setattr(model, x, json_post[x])
        model.save()
