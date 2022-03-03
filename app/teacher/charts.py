from app.models import Student


def chapter1_objectives(student_full_name):
    student = Student.query.filter_by(
        student_full_name=student_full_name).first()

    # CHAPTER 1: Calculate the number of objectives achieved
    all_objectives = student.webdev_chapter1_objectives.all()
    objectives_list = []
    num_of_true_status = 0
    for objective in all_objectives:
        objectives_list.append(str(objective.objective_1))
        objectives_list.append(str(objective.objective_2))
        objectives_list.append(str(objective.objective_3))
        objectives_list.append(str(objective.objective_4))
        objectives_list.append(str(objective.objective_5))
    num_of_true_status = objectives_list[-5:].count("True")
    try:
        percentage_achieved = round(
            (num_of_true_status / len(objectives_list[-5:])) * 100, 2
        )
    except ZeroDivisionError:
        percentage_achieved = 0

    # Chart for chapter 1 objectives
    objectives_attempts = {}
    for k, v in enumerate(all_objectives):
        objectives_attempts[k+1] = v
    print(objectives_attempts)
    print(len(objectives_list))
    chapter1_obj_attempts_chart_labels = list(objectives_attempts.keys())
    chapter1_obj_attempts_chart_data = []
    for i in range(0, len(objectives_list), 5):
        all_num_true_status = objectives_list[i:i+5].count("True")
        len_of_attempt = len(objectives_list[i:i+5])
        print(all_num_true_status, objectives_list[i:i+5])
        try:
            chapter1_obj_attempts_chart_data.append(
                round((all_num_true_status / len_of_attempt) * 100, 2))
        except ZeroDivisionError:
            chapter1_obj_attempts_chart_data.append(0)
    print('Chatper 1 Obj Labels: ', chapter1_obj_attempts_chart_labels)
    print('Chapter 1 Obj Values: ', chapter1_obj_attempts_chart_data, '\n\n')
    return percentage_achieved, chapter1_obj_attempts_chart_labels, \
        chapter1_obj_attempts_chart_data


def chapter2_objectives(student_full_name):
    student = Student.query.filter_by(
        student_full_name=student_full_name).first()

    # CHAPTER 2: Calculate the number of objectives achieved
    all_objectives_chapter_2 = student.webdev_chapter2_objectives.all()
    objectives_list_chapter_2 = []
    num_of_true_status_chapter_2 = 0
    for objective in all_objectives_chapter_2:
        objectives_list_chapter_2.append(str(objective.objective_1))
        objectives_list_chapter_2.append(str(objective.objective_2))
        objectives_list_chapter_2.append(str(objective.objective_3))
        objectives_list_chapter_2.append(str(objective.objective_4))
        objectives_list_chapter_2.append(str(objective.objective_5))
    num_of_true_status_chapter_2 = objectives_list_chapter_2[-5:].count("True")
    try:
        percentage_achieved_chapter_2 = round(
            (num_of_true_status_chapter_2 /
                len(objectives_list_chapter_2[-5:])) * 100, 2)
    except ZeroDivisionError:
        percentage_achieved_chapter_2 = 0

    # Chart for chapter 2
    objectives_attempts_chapter2 = {}
    for k, v in enumerate(all_objectives_chapter_2):
        objectives_attempts_chapter2[k+1] = v
    obj_attempts_chart_labels_chapter2 = list(
        objectives_attempts_chapter2.keys())
    obj_attempts_chart_data_chapter2 = []
    for i in range(0, len(objectives_list_chapter_2), 5):
        all_num_true_status_chapter2 = \
            objectives_list_chapter_2[i:i+5].count("True")
        len_of_attempt_chapter2 = len(objectives_list_chapter_2[i:i+5])
        print(
            all_num_true_status_chapter2, objectives_list_chapter_2[i:i+5])
        try:
            obj_attempts_chart_data_chapter2.append(
                round(
                    (all_num_true_status_chapter2 /
                        len_of_attempt_chapter2) * 100, 2))
        except ZeroDivisionError:
            obj_attempts_chart_data_chapter2.append(0)
    print('Chapter 2 Obj Labels: ', obj_attempts_chart_labels_chapter2)
    print('Chapter 2 Obj Values: ', obj_attempts_chart_data_chapter2, '\n\n')
    # End of Calculate the number of objectives achieved
    return percentage_achieved_chapter_2, obj_attempts_chart_labels_chapter2, \
        obj_attempts_chart_data_chapter2


def chapter3_objectives(student_full_name):
    student = Student.query.filter_by(
        student_full_name=student_full_name).first()

    # CHAPTER 3: Calculate the number of objectives achieved
    all_objectives_chapter_3 = student.webdev_chapter3_objectives.all()
    objectives_list_chapter_3 = []
    num_of_true_status_chapter_3 = 0
    for objective in all_objectives_chapter_3:
        objectives_list_chapter_3.append(str(objective.objective_1))
        objectives_list_chapter_3.append(str(objective.objective_2))
        objectives_list_chapter_3.append(str(objective.objective_3))
        objectives_list_chapter_3.append(str(objective.objective_4))
        objectives_list_chapter_3.append(str(objective.objective_5))
    num_of_true_status_chapter_3 = objectives_list_chapter_3[-5:].count("True")
    try:
        percentage_achieved_chapter_3 = round(
            (num_of_true_status_chapter_3 /
                len(objectives_list_chapter_3[-5:])) * 100, 2)
    except ZeroDivisionError:
        percentage_achieved_chapter_3 = 0

    # Chart for chapter 3
    objectives_attempts_chapter3 = {}
    for k, v in enumerate(all_objectives_chapter_3):
        objectives_attempts_chapter3[k+1] = v
    obj_attempts_chart_labels_chapter3 = list(
        objectives_attempts_chapter3.keys())
    obj_attempts_chart_data_chapter3 = []
    for i in range(0, len(objectives_list_chapter_3), 5):
        all_num_true_status_chapter3 = \
            objectives_list_chapter_3[i:i+5].count("True")
        len_of_attempt_chapter3 = len(objectives_list_chapter_3[i:i+5])
        print(
            all_num_true_status_chapter3, objectives_list_chapter_3[i:i+5])
        try:
            obj_attempts_chart_data_chapter3.append(
                round(
                    (all_num_true_status_chapter3 /
                        len_of_attempt_chapter3) * 100, 2))
        except ZeroDivisionError:
            obj_attempts_chart_data_chapter3.append(0)
    print('Chapter 3 Obj Labels: ', obj_attempts_chart_labels_chapter3)
    print('Chapter 3 Obj Values: ', obj_attempts_chart_data_chapter3, '\n\n')
    # End of Calculate the number of objectives achieved
    return percentage_achieved_chapter_3, obj_attempts_chart_labels_chapter3, \
        obj_attempts_chart_data_chapter3


def chapter1_total_score(student_full_name):
    student = Student.query.filter_by(
        student_full_name=student_full_name).first()

    chapter1_total_score = student.webdev_chapter1_quiz_total_scores.all()

    # Keys as labels for chatJS
    quiz_attempts_chapter1 = {}
    for k, v in enumerate(chapter1_total_score):
        quiz_attempts_chapter1[k+1] = v
    quiz_attempts_chart_labels_chapter1 = list(
        quiz_attempts_chapter1.keys())

    # Data as values for chatJS
    chapter1_total_score_list = []
    int_total_score_list_chapter1 = []
    for score in chapter1_total_score:
        chapter1_total_score_list.append(score.total_score)
    int_total_score_list_chapter1 = \
        [int(float(i)) for i in chapter1_total_score_list]
    print('Chapter 1 Quiz Total Score: ', chapter1_total_score_list, 'Length : ', len(chapter1_total_score_list), ' Keys: ', quiz_attempts_chart_labels_chapter1)
    print('Int total score list: ', int_total_score_list_chapter1)
    return int_total_score_list_chapter1, quiz_attempts_chart_labels_chapter1


def chapter2_total_score(student_full_name):
    student = Student.query.filter_by(
        student_full_name=student_full_name).first()

    chapter2_total_score = student.webdev_chapter2_quiz_total_scores.all()

    # Keys as labels for chatJS
    quiz_attempts_chapter2 = {}
    for k, v in enumerate(chapter2_total_score):
        quiz_attempts_chapter2[k+1] = v
    quiz_attempts_chart_labels_chapter2 = list(
        quiz_attempts_chapter2.keys())

    chapter2_total_score_list = []
    int_total_score_list_chapter2 = []
    for score in chapter2_total_score:
        chapter2_total_score_list.append(score.total_score)
    int_total_score_list_chapter2 = \
        [int(float(i)) for i in chapter2_total_score_list]
    print('Chapter 2 Quiz Total Score: ', chapter2_total_score_list, 'Length : ', len(chapter2_total_score_list), ' Keys: ', quiz_attempts_chart_labels_chapter2)
    return int_total_score_list_chapter2, quiz_attempts_chart_labels_chapter2


def chapter3_total_score(student_full_name):
    student = Student.query.filter_by(
        student_full_name=student_full_name).first()

    chapter3_total_score = student.webdev_chapter3_quiz_total_scores.all()

    # Keys as labels for chatJS
    quiz_attempts_chapter3 = {}
    for k, v in enumerate(chapter3_total_score):
        quiz_attempts_chapter3[k+1] = v
    quiz_attempts_chart_labels_chapter3 = list(
        quiz_attempts_chapter3.keys())

    chapter3_total_score_list = []
    int_total_score_list_chapter3 = []
    for score in chapter3_total_score:
        chapter3_total_score_list.append(score.total_score)
    int_total_score_list_chapter3 = \
        [int(float(i)) for i in chapter3_total_score_list]
    print('Chapter 3 Quiz Total Score: ', chapter3_total_score_list, 'Length : ', len(chapter3_total_score_list), ' Keys: ', quiz_attempts_chart_labels_chapter3)
    return int_total_score_list_chapter3, quiz_attempts_chart_labels_chapter3
