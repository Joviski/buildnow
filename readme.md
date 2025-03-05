# Subscription Management System

## Backend

- Implemented the necessary subscription logic, including creation, deletion, and auto-calculation of renewal dates.
- Developed a Celery task to handle auto-renewals and recalculate renewal dates.
- Calculated monthly expenses and incorporated all requested backend features.

  To run the project:
  server: python3 manage.py runserver 8007
  celery: celery -A subscription_cost.celery worker -l info

## Frontend

- Built a simple React app with a minimal design while achieving most of the requested features.
- Displayed all subscriptions related to the logged-in user.
  - Highlighted subscriptions with renewals within the next 7 days.
  - Showed the benefits of switching to an annual subscription.
- Visualized **monthly expenses for the last 6 months** using a bar chart.
- Integrated a calendar displaying upcoming subscription renewals.

  To run the project:
  npm start

## Possible Enhancements

- Implement **JWT authentication** instead of Basic Authentication.
- Use **Celery Beat** for automated renewals instead of manually scheduled Celery tasks.
- Improve the **dashboard design** for better user experience and aesthetics.

---

🚀 **This project provides a functional subscription management system with automated renewals, expense tracking, and a user-friendly interface.**

