from django.db import models

# Create your models here.
class FileModel(models.Model):
    file_name = models.CharField(max_length=50)
    file_content = models.FileField(upload_to="upload")
'''
class AlgorithmModel(models.Model):
    algorithm_name = models.CharField(max_length=50)
    inference_script = models.FileField(upload_to='algorithms/scripts/'
    saved_model = models.FileField(upload_to='algorithms/saved_models/')
    def __str__(self):
        return self.algorithm_name
    def delete(self, *args, **kwargs):
        self.inference_script.delete()
        self.saved_model.delete()
        super().delete(*args, **kwargs)
'''
class HistoryModel(models.Model):
    history_name = models.CharField(max_length=50)
    history_content = models.CharField(max_length = 10000)
