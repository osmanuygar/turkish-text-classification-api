from sentiment.db.model.dataset import Dataset, DatasetSchema, db, Model

dataset_schema = DatasetSchema()
datasets_schema = DatasetSchema(many=True)


def get_all_datasets():
    all_users = Dataset.query.all()
    result = datasets_schema.dump(all_users)
    return result


def add_new_dataset(content):
    text = content['text']
    model = content['model']
    category = content['category']
    label = content['label']
    new_dataset = Dataset(text=text, model=model, category=category, label=label)
    db.session.add(new_dataset)
    db.session.commit()


def update_dataset(id, content):
    dataset = Dataset.query.filter(Dataset.id == id).one()
    dataset.text = content.get('text')
    dataset.model = content.get('model')
    dataset.category = content.get('category')
    dataset.label = content.get('label')
    db.session.add(dataset)
    db.session.commit()


def delete_dataset(id):
    dataset = Dataset.query.filter(Dataset.id == id).one()
    db.session.delete(dataset)
    db.session.commit()


def add_new_model(model_name, model_type, score, threshold):
    new_model = Model(model_name=model_name, model_type=model_type, score=score, threshold=threshold)
    db.session.add(new_model)
    db.session.commit()


def delete_model(model_name):
    model = Model.query.filter(Model.model_name == model_name).one()
    db.session.delete(model)
    db.session.commit()
