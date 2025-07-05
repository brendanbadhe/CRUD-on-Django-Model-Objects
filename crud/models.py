from django.db import models
from django.utils.timezone import now


# User model
class User(models.Model):
    first_name = models.CharField(null=False, max_length=30, default="John")
    last_name = models.CharField(null=False, max_length=30, default="Doe")
    dob = models.DateField(null=True)

    # toString method
    def __str__(self):
        return self.first_name + " " + self.last_name


# Instructor model (One-to-one)
class Instructor(User):
    full_time = models.BooleanField(default=True)
    total_learners = models.IntegerField()

    # toString method
    def __str__(self):
        return (
            "First name: "
            + self.first_name
            + ", "
            + "Last name: "
            + self.last_name
            + ", "
            + "Is full time: "
            + str(self.full_time)
            + ", "
            + "Total Learners: "
            + str(self.total_learners)
        )


# Learner model
class Learner(User):
    STUDENT = "student"
    DEVELOPER = "developer"
    DATA_SCIENTIST = "data_scientist"
    DATABASE_ADMIN = "dba"
    # Enumeration to limit choices
    OCCUPATION_CHOICES = [
        (STUDENT, "Student"),
        (DEVELOPER, "Developer"),
        (DATA_SCIENTIST, "Data Scientist"),
        (DATABASE_ADMIN, "Database Admin"),
    ]
    occupation = models.CharField(
        null=False, max_length=20, choices=OCCUPATION_CHOICES, default=STUDENT
    )
    # URL Field
    social_link = models.URLField(max_length=200)

    # toString method
    def __str__(self):
        return (
            "First name: "
            + self.first_name
            + ", "
            + "Last name: "
            + self.last_name
            + ", "
            "Date of Birth: "
            + str(self.dob)
            + ", "
            + "Occupation: "
            + self.occupation
            + ", "
            + "Social Link: "
            + self.social_link
        )


# Course model (Many-to-many)
class Course(models.Model):
    name = models.CharField(null=False, max_length=100, default="online course")
    description = models.CharField(max_length=500)
    # Many-to-many relationships
    instructors = models.ManyToManyField(Instructor)
    learners = models.ManyToManyField(Learner, through="Enrollment")

    # toString method
    def __str__(self):
        return "Name: " + self.name + ", " + "Description: " + self.description


# Lesson model (One-to-many)
class Lesson(models.Model):
    title = models.CharField(max_length=200, default="title")
    course = models.ForeignKey(Course, null=True, on_delete=models.CASCADE)
    content = models.TextField()


# Enrollment model
class Enrollment(models.Model):
    AUDIT = "audit"
    HONOR = "honor"
    COURSE_MODES = [
        (AUDIT, "Audit"),
        (HONOR, "Honor"),
    ]
    learner = models.ForeignKey(Learner, on_delete=models.CASCADE)
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    date_enrolled = models.DateField(default=now)
    mode = models.CharField(max_length=5, choices=COURSE_MODES, default=AUDIT)
