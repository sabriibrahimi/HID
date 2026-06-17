
<p id="yui_3_18_1_1_1781694857419_364">You are tasked with creating a system for managing external collaborators (doctors) who cooperate with a hospital. The system should intuitively display all doctors according to their specialty and provide a detailed overview for each doctor with information about the appointments they have conducted, the appointments for the current day, and those scheduled for the future. Each doctor is characterized by a first name and last name, specialty (cardiologist, dermatologist, or neurologist), image, institution they come from, number of successfully completed appointments, contact email, and phone number. Each patient is characterized by a first name and last name, date of birth, gender, and contact email. Each appointment is characterized by appointment type (cardiology, dermatology, or neurology), symptom description, status (scheduled, in progress, completed), appointment date and time, and notes. One appointment must have one responsible doctor, but it may also have additional assistants (other doctors). One doctor can participate in multiple appointments, either as the responsible doctor or as an assistant. One patient can have multiple appointments at different dates and times.</p>

<ul>
<li>Doctors and patients can only be added by superusers.</li>
<li>Appointments can be added by all users who are doctors, but the user who creates the appointment automatically becomes the responsible doctor.</li>
<li>Appointments can only be modified by the doctor responsible for them or by a superuser.</li>
<li>An appointment can only be deleted if it has not started.</li>
<li>When an appointment in progress changes to completed status, only the responsible doctor should have their number of successfully completed appointments incremented.</li>
<li>Doctors can only view appointments for which they are responsible or assigned as assistants.</li>
</ul>

<span style="font-size: 0.9375rem; font-family: -apple-system, BlinkMacSystemFont, &quot;Segoe UI&quot;, Roboto, &quot;Helvetica Neue&quot;, Arial, &quot;Noto Sans&quot;, &quot;Liberation Sans&quot;, sans-serif, &quot;Apple Color Emoji&quot;, &quot;Segoe UI Emoji&quot;, &quot;Segoe UI Symbol&quot;, &quot;Noto Color Emoji&quot;;">In addition to the functionalities listed above, the following automatic validations and adjustments must be provided when adding or deleting data in the system (regardless of whether it is done through the admin panel or through a form).</span>

<ul id="yui_3_18_1_1_1781694857419_375">
<li>When adding a <strong>new</strong> <strong>appointment</strong> to the system:<br>
</li>
<ul id="yui_3_18_1_1_1781694857419_374">
<li>If the appointment is added with status completed, but its scheduled date and time are in the future, the system should automatically change the status to scheduled and vice versa, if it is added with status scheduled but the appointment date and time are in the past, then it should automatically be changed to completed.<br>
</li>
<li id="yui_3_18_1_1_1781694857419_373">(Bonus) If the doctor (as the responsible doctor) has appointments with three different patients from the same institution, then when adding a new appointment for a patient from that same institution, the appointment note should automatically be set to: "High workload with patients from institution {institution_name}".<br></li></ul></ul>

<li>When adding a <strong>new</strong> <strong>appointment</strong> to the system:<br>
</li>

<ul id="yui_3_18_1_1_1781694857419_374">
<li>If the appointment is added with status completed, but its scheduled date and time are in the future, the system should automatically change the status to scheduled and vice versa, if it is added with status scheduled but the appointment date and time are in the past, then it should automatically be changed to completed.<br>
</li>
<li id="yui_3_18_1_1_1781694857419_373">(Bonus) If the doctor (as the responsible doctor) has appointments with three different patients from the same institution, then when adding a new appointment for a patient from that same institution, the appointment note should automatically be set to: "High workload with patients from institution {institution_name}".<br></li></ul>

<span style="font-family: -apple-system, BlinkMacSystemFont, &quot;Segoe UI&quot;, Roboto, &quot;Helvetica Neue&quot;, Arial, &quot;Noto Sans&quot;, &quot;Liberation Sans&quot;, sans-serif, &quot;Apple Color Emoji&quot;, &quot;Segoe UI Emoji&quot;, &quot;Segoe UI Symbol&quot;, &quot;Noto Color Emoji&quot;; font-size: 0.9375rem;">Additionally, when a patient is deleted from the system, all of their appointments that have not yet started should be deleted, and for appointments that are currently in progress, the following note should be set: “Patient record missing – appointment preserved for audit purposes”.<br></span>

<span style="font-family: -apple-system, BlinkMacSystemFont, &quot;Segoe UI&quot;, Roboto, &quot;Helvetica Neue&quot;, Arial, &quot;Noto Sans&quot;, &quot;Liberation Sans&quot;, sans-serif, &quot;Apple Color Emoji&quot;, &quot;Segoe UI Emoji&quot;, &quot;Segoe UI Symbol&quot;, &quot;Noto Color Emoji&quot;; font-size: 0.9375rem;"><br>The web application consists of one home page that displays all doctors (grouped by specialty), and one page that provides a detailed overview for a specific doctor - including information about the doctor, all previous appointments, appointments for today, future appointments, as well as a form for adding a new appointment for that same doctor, where the appointment type will always correspond to the doctor's specialty. The pages are shown in the images below.</span>

<p><span style="font-size: 0.9375rem; font-family: -apple-system, BlinkMacSystemFont, &quot;Segoe UI&quot;, Roboto, &quot;Helvetica Neue&quot;, Arial, &quot;Noto Sans&quot;, &quot;Liberation Sans&quot;, sans-serif, &quot;Apple Color Emoji&quot;, &quot;Segoe UI Emoji&quot;, &quot;Segoe UI Symbol&quot;, &quot;Noto Color Emoji&quot;;"><strong>Automated Django Validation:</strong> The solution contains ready-made unit tests (in <em>hospital_app/tests/</em>) that test every aspect of the task (models, admin panel, signals, forms, views, and URL routing). The tests can be executed with the following command from the project's root directory:</span></p>

<p style="text-align: center;"><code>python manage.py check_solution</code></p>

<p><span style="font-size: 0.9375rem; font-family: -apple-system, BlinkMacSystemFont, &quot;Segoe UI&quot;, Roboto, &quot;Helvetica Neue&quot;, Arial, &quot;Noto Sans&quot;, &quot;Liberation Sans&quot;, sans-serif, &quot;Apple Color Emoji&quot;, &quot;Segoe UI Emoji&quot;, &quot;Segoe UI Symbol&quot;, &quot;Noto Color Emoji&quot;;">The expected result for a fully implemented solution is <strong>"ALL 64 TESTS PASS"</strong>. The test results are used as the basis for grading the Django part of the assignment (the Bootstrap part is graded manually).</span></p>

<p><span style="font-size: 0.9375rem; font-family: -apple-system, BlinkMacSystemFont, &quot;Segoe UI&quot;, Roboto, &quot;Helvetica Neue&quot;, Arial, &quot;Noto Sans&quot;, &quot;Liberation Sans&quot;, sans-serif, &quot;Apple Color Emoji&quot;, &quot;Segoe UI Emoji&quot;, &quot;Segoe UI Symbol&quot;, &quot;Noto Color Emoji&quot;;"><strong>Note: The assignment will not be reviewed if the solution does not compile, i.e. the server does not start successfully!</strong><br></span></p>

<p id="yui_3_18_1_1_1781694857419_366"><span style="font-size: 0.9375rem; font-family: -apple-system, BlinkMacSystemFont, &quot;Segoe UI&quot;, Roboto, &quot;Helvetica Neue&quot;, Arial, &quot;Noto Sans&quot;, &quot;Liberation Sans&quot;, sans-serif, &quot;Apple Color Emoji&quot;, &quot;Segoe UI Emoji&quot;, &quot;Segoe UI Symbol&quot;, &quot;Noto Color Emoji&quot;;"><strong><br></strong></span></p>
```
