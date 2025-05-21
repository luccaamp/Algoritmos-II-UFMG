// Exemplo de rolagem suave
document.querySelectorAll('a[href^="#"]').forEach(anchor => {
    anchor.addEventListener('click', function (e) {
        e.preventDefault();
        document.querySelector(this.getAttribute('href')).scrollIntoView({
            behavior: 'smooth'
        });
    });
});

/*         // Lista dos arquivos de imagem
        const images = [
            "./assets/images/step1.png",
            "./assets/images/step2.png",
            "./assets/images/step3.png",
            "./assets/images/step4.png",
            "./assets/images/step5.png",
            "./assets/images/step6.png",
            "./assets/images/step7.png",
        ];
        let currentIndex = 0;

        // Referências aos elementos
        const carouselImage = document.getElementById("carouselImage");
        const prevBtn = document.getElementById("prevBtn");
        const nextBtn = document.getElementById("nextBtn");

        // Função para atualizar a imagem
        function updateImage() {
            carouselImage.src = images[currentIndex];
            carouselImage.alt = `Etapa ${currentIndex + 1}`;
            prevBtn.disabled = currentIndex === 0;
            nextBtn.disabled = currentIndex === images.length - 1;
        }

        // Navegar para a imagem anterior
        function prevImage() {
            if (currentIndex > 0) {
                currentIndex--;
                updateImage();
            }
        }

        // Navegar para a próxima imagem
        function nextImage() {
            if (currentIndex < images.length - 1) {
                currentIndex++;
                updateImage();
            }
        } */

// Lista de imagens e controle de índice
const images = ["./assets/images/step1.png", "./assets/images/step2.png", "./assets/images/step3.png", "./assets/images/step4.png", "./assets/images/step5.png", "./assets/images/step6.png", "./assets/images/step7.png"];
let currentIndex = 0;

// Referências dos elementos HTML
const imgElement = document.getElementById("carouselImage");
const prevBtn = document.getElementById("prevBtn");
const nextBtn = document.getElementById("nextBtn");

// Função para atualizar a imagem do carrossel
function updateImage() {
    imgElement.src = images[currentIndex];
    prevBtn.disabled = currentIndex === 0;
    nextBtn.disabled = currentIndex === images.length - 1;
}

// Eventos dos botões
function nextImage() {
    if (currentIndex < images.length - 1) {
        currentIndex++;
        updateImage();
    }
}

function prevImage() {
    if (currentIndex > 0) {
        currentIndex--;
        updateImage();
    }
}

// Inicializar a exibição ao carregar a página
window.onload = function () {
    updateImage(); // Exibe a primeira imagem
};
