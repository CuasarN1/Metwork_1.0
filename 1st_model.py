from imageai.Classification.Custom import ClassificationModelTrainer

model_trainer = ClassificationModelTrainer()
model_trainer.setModelTypeAsResNet50()
model_trainer.setDataDirectory('path')
model_trainer.trainModel(num_objects=2, num_experiments=190, enhance_data=True, batch_size=32, show_network_summary=True)
