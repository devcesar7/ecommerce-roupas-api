// static/produtos/js/produto_detalhe.js

document.addEventListener('DOMContentLoaded', () => {
    // Lógica para as abas (DETALHES DO PRODUTO, INFORMAÇÕES)
    const tabButtons = document.querySelectorAll('.tab-button');
    const tabContents = document.querySelectorAll('.tab-content');

    tabButtons.forEach(button => {
        button.addEventListener('click', () => {
            // Remove a classe 'active' de todos os botões e conteúdos
            tabButtons.forEach(btn => btn.classList.remove('active'));
            tabContents.forEach(content => content.classList.remove('active'));

            // Adiciona a classe 'active' ao botão clicado e ao conteúdo correspondente
            const tabId = button.getAttribute('data-tab');
            document.getElementById(tabId).classList.add('active');
            button.classList.add('active');
        });
    });

    // --- Nova Lógica para o Carrossel de Imagens ---
    const mainImage = document.getElementById('main-product-image');
    const thumbnails = document.querySelectorAll('.thumbnail');

    thumbnails.forEach(thumbnail => {
        thumbnail.addEventListener('click', function() {
            // Remove a classe 'active' de todas as miniaturas
            thumbnails.forEach(t => t.classList.remove('active'));

            // Adiciona a classe 'active' à miniatura clicada
            this.classList.add('active');

            // Troca a imagem principal pela imagem da miniatura clicada
            const fullSizeSrc = this.getAttribute('data-full-size-src');
            mainImage.src = fullSizeSrc;
        });
    });
});