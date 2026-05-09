from django.db import models

class Department(models.Model):
    """
    Represents a major academic unit (e.g., School of Information Technology).
    """
    name = models.CharField(max_length=255, unique=True)
    code = models.CharField(max_length=50, unique=True)
    description = models.TextField(blank=True, null=True)
    # You could add a head_of_department = models.ForeignKey(User, ...) here if needed

    def __str__(self):
        return self.name

class Program(models.Model):
    """
    Represents a specific academic program/discipline within a department
    (e.g., BS Computer Science under NUSIT).
    """
    department = models.ForeignKey(Department, on_delete=models.CASCADE, related_name='programs')
    name = models.CharField(max_length=255)
    code = models.CharField(max_length=50, unique=True)
    description = models.TextField(blank=True, null=True)

    class Meta:
        unique_together = ('department', 'name') # A program name must be unique within a department

    def __str__(self):
        return f"{self.code} ({self.department.code})"
