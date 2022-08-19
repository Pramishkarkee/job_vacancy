const confirmVacancyDelete = (vacancyId) => {
  Swal.fire({
    title: 'Are you sure you want to delete this vacancy?',
    text: 'This action cannot be reverted.',
    icon: 'warning',
    width: '40rem',
    showCancelButton: true,
    confirmButtonColor: '#d33',
    cancelButtonColor: '#7e8780',
    confirmButtonText: 'Delete',
  }).then((result) => {
    if (result.isConfirmed) {
      document.getElementById(`delete-vacancy-link-${vacancyId}`).click();
      Swal.fire({
        position: 'top-end',
        icon: 'success',
        title: 'The vacancy has been deleted successfully.',
        toast: true,
        timerProgressBar: true,
        showConfirmButton: false,
        timer: 1500,
      });
    }
  });
};
