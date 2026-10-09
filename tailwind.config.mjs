/**
 * Locanda Seggiovia — token di brand.
 *
 * NOTA IMPORTANTE SUL FUNZIONAMENTO
 * ---------------------------------
 * Il progetto usa Tailwind CSS v4. In v4 la configurazione è "CSS-first":
 * la fonte di verità dei design token è il blocco `@theme` in
 * `src/styles/global.css`, che genera anche le variabili CSS usate nei
 * template (es. `var(--color-stone-100)`).
 *
 * Questo file resta come documento di riferimento del brand: elenca palette,
 * tipografia, scala tipografica e spaziature. Se in futuro servisse caricarlo
 * davvero in Tailwind, basta aggiungere in cima a `global.css`:
 *
 *     @config "../../tailwind.config.mjs";
 *
 * Verificare in quel caso che il build includa ancora tutte le variabili.
 */

/** @type {import('tailwindcss').Config} */
export default {
  content: ['./src/**/*.{astro,html,js,jsx,md,mdx,ts,tsx}'],

  theme: {
    extend: {
      colors: {
        // Pietra alpina — grigi caldi, base di tutto il sito.
        stone: {
          50: '#FAF9F6',
          100: '#F2F0EB',
          200: '#E5E1D8',
          300: '#CFCABE',
          400: '#948F84',
          500: '#6E6A61',
          600: '#4F4C46',
          700: '#37352F',
          800: '#232220',
          900: '#1C1B19',
        },
        // Legno — superfici scure, ristorante, footer.
        wood: {
          100: '#E8DFD3',
          300: '#C0A583',
          500: '#8A6A45',
          700: '#3F2F21',
          900: '#2E2218',
        },
        // Verde bosco — accenti, link, conferme.
        forest: {
          100: '#E1E6DF',
          300: '#A8B5A2',
          500: '#5A7A5E',
          700: '#2D3D31',
          900: '#1E2A21',
        },
        // Albero/rosa alpino — micro-accento, usato con parsimonia.
        glow: {
          300: '#D8B3A3',
          500: '#B5735C',
        },
      },

      fontFamily: {
        // Titoli: serif con optical size, evoca l'insegna dipinta e i
        // manifesti storici delle valli.
        display: ['Fraunces', 'ui-serif', 'Georgia', 'Cambria', 'Times New Roman', 'serif'],
        // Corpo: stack di sistema, zero richieste di rete (§ performance).
        sans: [
          'ui-sans-serif',
          'system-ui',
          '-apple-system',
          'Segoe UI',
          'Roboto',
          'Helvetica Neue',
          'Arial',
          'sans-serif',
        ],
      },

      fontSize: {
        // Scala sobria: rapporto ~1.25, adatta a un sito editoriale.
        xs: ['0.75rem', { lineHeight: '1.5' }],
        sm: ['0.875rem', { lineHeight: '1.6' }],
        base: ['1.0625rem', { lineHeight: '1.7' }],
        lg: ['1.25rem', { lineHeight: '1.65' }],
        xl: ['1.5rem', { lineHeight: '1.4' }],
        '2xl': ['1.875rem', { lineHeight: '1.3' }],
        '3xl': ['2.375rem', { lineHeight: '1.2' }],
        '4xl': ['3rem', { lineHeight: '1.12' }],
        '5xl': ['3.75rem', { lineHeight: '1.05' }],
        '6xl': ['4.75rem', { lineHeight: '1' }],
      },

      maxWidth: {
        // Lunghezza di riga sotto gli 80 caratteri (§ tipografia).
        prose: '68ch',
        shell: '76rem',
      },

      spacing: {
        section: 'clamp(4.5rem, 11vw, 9.5rem)',
      },

      transitionTimingFunction: {
        alpine: 'cubic-bezier(0.22, 1, 0.36, 1)',
      },
    },
  },

  plugins: [],
};
