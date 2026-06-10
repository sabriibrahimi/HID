# Define your signal receivers here.
from django.db.models.signals import pre_save, pre_delete
from django.dispatch import receiver
from django.utils.timezone import now

from .models import Appointment, Patient

@receiver(pre_save,sender=Appointment)
#If the examination is added with status completed, but its appointment term is in the future, the system will automatically change its status to scheduled and vice versa, if it is added with
# status scheduled in the past, then it will automatically be changed to complete.
def status_changing(sender, instance, **kwargs):
    if instance.status == 'completed' and instance.datetime > now():
        instance.status = 'scheduled'

    if instance.status == 'scheduled' and instance.datetime < now():
        instance.status = 'completed'

#(Bonus) If the doctor (as responsible) has examinations with three different
# patients from the same institution, then when adding a new examination for a patient from the same institution,
# the following note will automatically be set in the examination:
# High workload with patients from institution {institution_name}.

    if instance.pk:
        return

    doctor = instance.responsible_doctor
    patient = instance.patient
    institution_name = patient.institution

    patient_count = Appointment.objects.filter(
        responsible_doctor=doctor,
        patient__institution=institution_name
    ).values_list('patient_id',flat=True).distinct().count()

    if patient_count >= 3:
        instance.note = f"High workload with patients from institution {institution_name}"


# When a patient is deleted from the system, all of their examinations
# that have not yet started should be deleted,
# and for the examinations that are in progress — the following note should be set:
# Patient record missing – appointment preserved for audit purposes
@receiver(pre_delete, sender=Patient)
def deletion_of_patient(sender, instance, **kwargs):
    appointments = Appointment.objects.filter(patient=instance)

    for appointment in appointments:
        if appointment.status == 'scheduled':
            appointment.delete()

        elif appointment.status == 'in_progress':
            appointment.note = (
                "Patient record missing - appointment preserved for audit purposes"
            )
            appointment.patient = None
            appointment.save()
