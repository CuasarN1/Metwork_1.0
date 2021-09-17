from imageai.Classification.Custom import ClassificationModelTrainer


model_trainer = ClassificationModelTrainer()
model_trainer.setModelTypeAsInceptionV3()
model_trainer.setDataDirectory('../dataset/')
model_trainer.trainModel(num_objects=2, num_experiments=3, enhance_data=True
                         , batch_size=4, show_network_summary=True)
