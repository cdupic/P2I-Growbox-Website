document.addEventListener("DOMContentLoaded", () => {
    const AUTO_SUBMIT_DELAY = 1500;

    const forms = document.querySelectorAll('form.auto-submit');

    forms.forEach(form => {
        const inputs = form.querySelectorAll('input, textarea, select');
        inputs.forEach(input => {
            let timeout;
            let previousValue = input.value;

            if (input.type === 'date'){
                // Handle date inputs separately
                input.addEventListener('change', () => {
                    if(input.value !== previousValue){
                        form.submit();
                    }
                });

                input.addEventListener('input', () => {
                    clearTimeout(timeout);
                    timeout = setTimeout(() => {
                        if(input.value !== previousValue){
                            form.submit();
                        }
                    }, AUTO_SUBMIT_DELAY);
                });
            }else if(input.type === 'checkbox'){
                input.addEventListener('change', () => {
                    timeout = setTimeout(() => {
                        form.submit();
                    }, 200);
                });
            } else {
                input.addEventListener('input', () => {
                    clearTimeout(timeout);
                    timeout = setTimeout(() => {
                        if (input.value !== previousValue) {
                            form.submit();
                        }
                    }, AUTO_SUBMIT_DELAY);
                });
            }
        });
    });
});
