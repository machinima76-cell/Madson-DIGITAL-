/* ==========================================================================
   MADSON DIGITAL — Configuração central
   --------------------------------------------------------------------------
   Este é o ÚNICO arquivo a editar para trocar canais de contato.
   main.js aplica estes valores a todos os links e ao formulário.

   Os links estáticos no HTML já trazem os valores atuais como fallback para
   visitantes sem JavaScript; ao editar este arquivo, atualize também os
   atributos href marcados com data-whatsapp / data-email (ver README.md).

   siteUrl: SUBSTITUA pelo domínio definitivo (ou pelo domínio *.pages.dev
   gerado pela Cloudflare) antes de publicar. Ele é usado em canonical,
   Open Graph, sitemap.xml e robots.txt.
   ========================================================================== */
window.MADSON_CONFIG = {
  brand: 'MADSON DIGITAL',

  // DDI + DDD + número, somente dígitos. Ex.: 5547997139043
  whatsapp: '5547997139043',

  // E-mail de destino do formulário e do link de contato
  email: 'madsonsantos661@gmail.com',

  // Domínio canônico de publicação (trocar no deploy)
  siteUrl: 'https://madson-digital.pages.dev',

  // Mensagem inicial dos links diretos de WhatsApp
  whatsappGreeting: 'Olá! Vim pelo site da Madson Digital e gostaria de solicitar um orçamento.',

  // Redes sociais oficiais. Nenhuma foi informada, portanto a coluna do
  // rodapé permanece oculta (não criamos links inexistentes).
  // Para ativar, adicione: { name: 'Instagram', url: 'https://instagram.com/seuperfil' }
  socials: []
};
