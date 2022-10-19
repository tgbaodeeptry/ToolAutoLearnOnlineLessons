from apscheduler.schedulers.blocking import BlockingScheduler

import database
import autobroswer
import lms
import fb
import time
import proxy

# connect firebase
database.connect()


def learn(ip):
    data = database.get_all_info()

    for user in data.keys():
        print("User learning: " + user)
        password = data[user]["password"]
        id_fb = data[user]["id"]

        autobroswer.create_new_browser(ip)
        autobroswer.login_to_lms(user, password)

        ids_to_view_pre = lms.get_ids_courses_not_finished(autobroswer.get_course_data())
        data_before = lms.get_progress(autobroswer.get_course_data())

        if len(ids_to_view_pre) == 0:
            autobroswer.cancel()
            continue

        autobroswer.view_courses_not_finished(ids_to_view_pre)

        data_after = lms.get_progress(autobroswer.get_course_data())
        messages = "Tiến trình học: \n"
        messages += "----------------------------\n"

        for id in ids_to_view_pre:
            messages += f"Môn: {data_after[id]['name']} \n"
            messages += f"  + Trước: {data_before[id]['progress']}% \n"
            messages += f"  + Giờ: {data_after[id]['progress']}% \n\n"

        fb.send_messages(id_fb, messages)

        autobroswer.cancel()


def tries():
    print("Learning ......")
    found = False
    tested = []

    while not found:
        ips = proxy.get_ips()

        for ip in ips:
            if ip in tested:
                continue

            tested.append(ip)

            print("Testing: " + ip)

            success = autobroswer.create_new_browser(ip, test=True)

            if not success:
                time.sleep(10)
                continue

            print("Using IP: " + ip)

            # proxy work
            learn(ip)
            found = True

            print("Finished!")
            print("--------------------")

            break


scheduler = BlockingScheduler()


@scheduler.scheduled_job('cron', day_of_week="thu", hour='13-15', minute="15")
def scheduled_job():
    tries()


scheduler.start()
