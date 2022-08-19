applyNow.addEventListener('click', () => {
  Swal.fire({
    title: 'Do you want to apply for this job?',
    text:
      'You will receive an email from the provider as a follow-up to your application.',
    icon: 'info',
    width: '40rem',
    showCancelButton: true,
    confirmButtonColor: '#3085d6',
    cancelButtonColor: '#d33',
    confirmButtonText: 'Apply Now',
  }).then((result) => {
    if (result.isConfirmed) {
      document.getElementById('apply-link').click();
      Swal.fire({
        position: 'top-end',
        icon: 'success',
        title: 'You have applied for this job. Good Luck!',
        toast: true,
        timerProgressBar: true,
        showConfirmButton: false,
        timer: 1500,
      });
    }
  });
});
