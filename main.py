import re

students = {}

courses = {
    'Python': {
        'credits': 600,
        'enrolled': 0,
        'submission': 0,
        'points': 0,
    },
    'DSA': {
        'credits': 400,
        'enrolled': 0,
        'submission': 0,
        'points': 0,
    },
    'Databases': {
        'credits': 480,
        'enrolled': 0,
        'submission': 0,
        'points': 0,
    },
    'Flask': {
        'credits': 550,
        'enrolled': 0,
        'submission': 0,
        'points': 0,
    },
}


def is_valid_name(name_to_check):
    if re.match("^[a-zA-Z][a-zA-Z'\-]*[a-zA-Z]$", name_to_check):
        if re.search(r"-'", name_to_check) or re.search(r"'-", name_to_check) \
                or re.search(r"--", name_to_check) or re.search(r"''", name_to_check):
            return False
        return True
    return False


def is_valid_email(email):
    if re.match("^[a-zA-Z0-9.]+@[a-zA-Z0-9]+\.[a-zA-Z0-9]+$", email):
        return True
    return False


def is_valid_last_name(last_name: str):
    if ' ' in last_name:
        last_name_array = last_name.strip().split(' ')
        for last_names in last_name_array:
            return is_valid_name(last_names)
    else:
        return is_valid_name(last_name)


def valid_credentials(first_name, last_name, email):
    if not is_valid_name(first_name):
        print('Incorrect first name.')
        return False
    if not is_valid_last_name(last_name):
        print('Incorrect last name.')
        return False
    if not is_valid_email(email):
        print('Incorrect email.')
        return False
    return True


def add_student(email, first_name, last_name):
    students[email] = {
        'id': hash(email) % 100000,
        'first_name': first_name,
        'last_name': last_name,
    }
    students[email]['points'] = {a_course: 0 for a_course in courses}


def update_student_points(student_id, python_pts, dsa_pts, databases_pts, flask_pts):
    for emailAccount in students:
        if str(students[emailAccount]['id']) == student_id:
            students[emailAccount]['points']['Python'] += int(python_pts)
            students[emailAccount]['points']['DSA'] += int(dsa_pts)
            students[emailAccount]['points']['Databases'] += int(databases_pts)
            students[emailAccount]['points']['Flask'] += int(flask_pts)
            update_courses(
                [
                    students[emailAccount]['points']['Python'],
                    students[emailAccount]['points']['DSA'],
                    students[emailAccount]['points']['Databases'],
                    students[emailAccount]['points']['Flask']
                ]
            )
            return True
    return False


def update_courses(course_pts_list):
    index = 0
    course_keys = list(courses.keys())

    for course_pt in course_pts_list:
        a_course = course_keys[index]
        if course_pt:
            courses[a_course]['enrolled'] += 1
            courses[a_course]['submission'] += 1
            courses[a_course]['points'] += course_pts_list[index]
        index += 1


def list_students():
    if len(students.keys()):
        print('Students:')
        for emailAccount in students:
            print(students[emailAccount]['id'])
    else:
        print('No students found.')


def find_student(student_id):
    for emailAccount in students:
        if str(students[emailAccount]['id']) == student_id:
            output = f'{student_id} points: '
            for point in students[emailAccount]['points']:
                output += f"{point}={students[emailAccount]['points'][point]}; "
            print(output.strip()[:len(output) - 2])
            return True
    return False


def calculate_highest_popularity_or_submission(key):
    highest = 1
    highest_list = []

    for a_course, course_data in courses.items():
        value = course_data[key]

        if value > highest:
            highest = value
            highest_list = [a_course]
        elif value == highest:
            highest_list.append(a_course)

    return ', '.join(highest_list).strip() or 'n/a'


def calculate_least_popularity_or_submission(key):
    least = -1
    least_list = []

    for a_course, course_data in courses.items():
        value = course_data[key]
        if value < least:
            least = value
            least_list = [a_course]
        elif value == least:
            least_list.append(a_course)

    return ', '.join(least_list).strip() or 'n/a'


def calculate_highest_score():
    highest_score = 0
    highest_score_list = []

    for a_course, course_data in courses.items():
        points = course_data['points']
        submission = course_data['submission']

        if submission > 0:
            avg_score = points / submission
            if avg_score > highest_score:
                highest_score = avg_score
                highest_score_list = [a_course]
            elif avg_score == highest_score:
                highest_score_list.append(a_course)

    return ', '.join(highest_score_list).strip() or 'n/a'


def calculate_lowest_score():
    least_score = float('inf')
    least_score_list = []

    for a_course, course_data in courses.items():
        points = course_data['points']
        submission = course_data['submission']

        if submission > 0:
            avg_score = points / submission
            if avg_score < least_score:
                least_score = avg_score
                least_score_list = [a_course]
            elif avg_score == least_score:
                least_score_list.append(a_course)

    return ', '.join(least_score_list).strip() or 'n/a'


def print_statistics():
    print('Most popular:', calculate_highest_popularity_or_submission('enrolled'))
    print('Least popular:', calculate_least_popularity_or_submission('enrolled'))
    print('Highest activity:', calculate_highest_popularity_or_submission('submission'))
    print('Lowest activity:', calculate_least_popularity_or_submission('submission'))
    print('Easiest course:', calculate_highest_score())
    print('Hardest course:', calculate_lowest_score())


def find_top_learners(a_course):
    top_score_list = []

    for student_email, student_data in students.items():
        point = student_data['points'][a_course]
        if point:
            completed_percentage = round((point / courses[a_course]['credits']) * 100, 1)
            student = (student_data['id'], point, completed_percentage)
            top_score_list.append(student)

    top_score_list.sort(key=lambda x: (-x[1], x[0]))
    return top_score_list


def display_top_learners(a_course):
    if a_course == 'dsa':
        a_course = a_course.upper()
    else:
        a_course = a_course.capitalize()
    print(a_course)
    print(f'id\tpoints\tcompleted')
    sorted_top_learners = find_top_learners(a_course)
    print(
        *[f'{top_learner[0]}\t{top_learner[1]}\t\t{top_learner[2]}%'
          for top_learner in sorted_top_learners if top_learner[1] > 0], sep='\n'
    )


if __name__ == '__main__':
    count = 0
    print("Learning Progress Tracker")
    while True:
        user_read = input().strip().lower()
        if user_read == 'exit':
            print('Bye!')
            break
        elif user_read == 'back':
            print("Enter 'exit' to exit the program")
        elif user_read == '':
            print('No input')
            continue
        elif user_read == 'add students':
            print('Enter student credentials or "back" to return:')
            while True:
                student_credentials = input()
                if student_credentials == 'back':
                    print(f'Total {count} students have been added')
                    break
                else:
                    try:
                        name, email_account = student_credentials.strip().rsplit(' ', 1)
                        first, last = name.strip().split(' ', 1)

                        if not valid_credentials(first, last, email_account):
                            continue
                        else:
                            if email_account in students:
                                print('This email is already taken.')
                                continue
                            else:
                                add_student(email_account, first, last)
                                print('The student has been added.')
                                count += 1
                    except ValueError:
                        print('Incorrect credentials.')
                        continue

        elif user_read == 'list':
            list_students()

        elif user_read == 'add points':
            print("Enter an id and points or 'back' to return")
            while True:
                id_and_points = input().strip()
                if id_and_points == 'back':
                    break
                matched = re.match(r"^([a-zA-Z0-9]+) ([0-9]+) ([0-9]+) ([0-9]+) ([0-9]+)$", id_and_points)
                if matched:
                    stud_id, python, dsa, databases, flask = matched.groups()
                    if update_student_points(stud_id, python, dsa, databases, flask):
                        print('Points updated.')
                    else:
                        print(f'No student is found for id={stud_id}')
                else:
                    print('Incorrect points format.')
                    continue

        elif user_read == 'find':
            print("Enter an id or 'back' to return")
            while True:
                user_entered_id = input().strip()
                if user_entered_id == 'back':
                    break
                if find_student(user_entered_id):
                    continue
                else:
                    print(f'No student is found for id={user_entered_id}')
                    continue

        elif user_read == 'statistics':
            print("Type the name of a course to see details or 'back' to quit")
            print_statistics()
            while True:
                course = input().strip().lower()
                if course == 'back':
                    break
                courses_list = [course.lower() for course in courses.keys()]
                if course in courses_list:
                    display_top_learners(course)
                else:
                    print('Unknown course.')

        else:
            print('Unknown command!')
