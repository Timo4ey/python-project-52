# Test suites for task manager

---
### 1. Task's test suit
1. Test Views
   1. Positive scenario [If user login]
      1. page `tasks/` Response 200
      1. page `tasks/create` Response 200
      2. 
      1. page `tasks/delete` Response 200 if delete a task created by the user
      1. page `tasks/delete` Response 403 if delete a task created by another user
   1. Negative scenario
      1. If not login page `tasks/` Response 403
      2. If user login page `tasks/create` Response 403