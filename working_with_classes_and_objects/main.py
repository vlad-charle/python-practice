from university import Student, Professor, Lecture

john_doe = Student("John", "Doe", 21, ["History"])
john_doe.print_full_name()
john_doe.list_lectures()
john_doe.attend_new_lecture("Math")
john_doe.leave_lecture("CS50")

nancy_dryu = Professor("Nancy", "Dryu", 49, ["History"])
nancy_dryu.print_full_name()
nancy_dryu.list_subjects()
nancy_dryu.teach_new_subject("Math")
nancy_dryu.remove_subject("History")

history = Lecture("History", 5, 90, ["Suzzy Quatro"])
history.print_lecture_and_duration()
history.add_professor("John Doe")