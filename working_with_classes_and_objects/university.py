class Person:
    def __init__(self, first_name, last_name, age):
        self.first_name = first_name
        self.last_name = last_name
        self.age = age

    def print_full_name (self):
        print(f"Person's full name is: {self.first_name} {self.last_name}")

class Student(Person):
    def __init__ (self, first_name, last_name, age, lectures = []):
        super().__init__(first_name, last_name, age)
        self.lectures = lectures
    
    def print_full_name (self):
        Person.print_full_name(self)

    def list_lectures (self):
        if self.lectures == []:
            print(f"{self.first_name} {self.last_name} doesn't attend any lectures")
        else:
            print(f"{self.first_name} {self.last_name} attends following lectures:")
            for lecture in self.lectures:
                print(lecture)
    
    def attend_new_lecture (self, new_lecture: str):
        self.lectures.append(new_lecture)
        print(f"Lecture {new_lecture} added. Your updated list of lectures looks like this:")
        for lecture in self.lectures:
            print(lecture)

    def leave_lecture (self, lecture_to_leave: str):
        if self.lectures == []:
            print("You don't attend any lectures")
        else:
            if lecture_to_leave in self.lectures:
                self.lectures.remove(lecture_to_leave)
                print(f"Lecture {lecture_to_leave} removed. Your updated list of lectures looks like this:")
                for lecture in self.lectures:
                    print(lecture)
            else:
                print("I'm sorry, but you don't attend this lecture")

class Professor(Person):
    def __init__ (self, first_name, last_name, age, subjects = []):
        super().__init__(first_name, last_name, age)
        self.subjects = subjects
    
    def print_full_name (self):
        Person.print_full_name(self)

    def list_subjects (self):
        if self.subjects == []:
            print(f"{self.first_name} {self.last_name} doesn't teach any subjects")
        else:
            print(f"{self.first_name} {self.last_name} teach following subjects:")
            for subject in self.subjects:
                print(subject)

    def teach_new_subject (self, new_subject: str):
        self.subjects.append(new_subject)
        print(f"Subject {new_subject} added. Your updated list of subjects looks like this:")
        for subject in self.subjects:
            print(subject)

    def remove_subject (self, subject_to_remove: str):
        if self.subjects == []:
            print("You don't teach any subjects")
        else:
            if subject_to_remove in self.subjects:
                self.subjects.remove(subject_to_remove)
                print(f"Subject {subject_to_remove} removed. Your updated list of subjects looks like this:")
                for subject in self.subjects:
                    print(subject)
            else:
                print("I'm sorry, but you don't teach this subject")

class Lecture:
    def __init__(self, name, max_students: int, duration: int, professors_list = []):
        self.name = name
        self.max_students = max_students
        self.duration = duration
        self.professors_list = professors_list

    def print_lecture_and_duration (self):
        print(f"Lecture name is {self.name} and it's duration is {self.duration} minutes")

    def add_professor (self, professor_name):
        self.professors_list.append(professor_name)
        print(f"Updated list of professors looks like this:")
        for professor in self.professors_list:
            print(professor)
