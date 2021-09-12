from imageai.Classification.Custom import ClassificationModelTrainer


model_trainer = ClassificationModelTrainer()
model_trainer.setModelTypeAsResNet50()
model_trainer.setDataDirectory('../dataset/')
model_trainer.trainModel(num_objects=2, num_experiments=1, enhance_data=False
                         , batch_size=16, show_network_summary=True)
