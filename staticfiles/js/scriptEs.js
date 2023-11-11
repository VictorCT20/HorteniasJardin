window.addEventListener("DOMContentLoaded", () => {
    const starRating = new StarRating("#form");
});

class StarRating {
    constructor(qs) {
        this.ratings = [
            { id: 1 },
            { id: 2 },
            { id: 3 },
            { id: 4 },
            { id: 5 }
        ];
        this.rating = null;
        this.el = document.querySelector(qs);

        this.init();
    }

    init() {
        if (this.el && this.el.tagName === 'FORM'){

			this.el.addEventListener("change", this.updateRating.bind(this));
		}

        // stop Firefox from preserving form data between refreshes
        try {
            this.el.reset();
        } catch (err) {
            console.error("Element isn’t a form.");
        }

        const commentForm = document.getElementById("commentForm");
        const commentsTextarea = document.getElementById("comments");
        const displayComments = document.getElementById("displayComments");

        const updateRating = (e) => {
            const ratingObject = e.target.value;
            const displayComment = displayComments.querySelector(`[data-rating="${ratingObject}"]`);

            commentForm.style.display = "block"; // Mostrar el formulario de comentarios
            commentsTextarea.value = ""; // Limpiar el área de comentarios

            // Mostrar el área de comentarios solo si hay comentarios previos para la misma calificación
            if (displayComment && displayComment.textContent.trim() !== "") {
                commentsTextarea.value = displayComment.textContent.trim();
            }
        };

        const submitComment = () => {
            const selectedRating = document.querySelector('input[name="rating"]:checked');
            const displayComment = displayComments.querySelector(`[data-rating="${selectedRating.value}"]`);

            // Guardar el comentario
            displayComment.textContent = commentsTextarea.value;

            // Ocultar el formulario de comentarios después de enviar
            commentForm.style.display = "none";
        };

        const ratingInputs = document.querySelectorAll('input[name="rating"]');
        ratingInputs.forEach(input => {
            input.addEventListener("change", updateRating);
        });

        const submitButton = document.querySelector('.submitButton');
        submitButton.addEventListener("click", submitComment);
    }
}
