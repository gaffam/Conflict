const OYUN_VERISI = {
  EN: [
    { gibberish: 'bee 4 you go', answer: 'before you go' },
    { gibberish: 'see view later', answer: 'see you later' },
    { gibberish: 'loaf yore navel', answer: 'love your neighbor' },
  ],
  HE: [
    { gibberish: 'כוף משח קר', answer: 'קוף משקר' },
    { gibberish: 'ביטה בלה ביזה', answer: 'ביתה בלב העיר' },
    { gibberish: 'שלוש נדב ין', answer: 'שלום עליכם' },
  ],
};

function ShelterGame({ lang = 'EN' }) {
  const [index, setIndex] = React.useState(() => Math.floor(Math.random() * (OYUN_VERISI[lang]?.length || 1)));
  const [show, setShow] = React.useState(false);

  React.useEffect(() => {
    newGame();
  }, [lang]);

  function newGame() {
    const list = OYUN_VERISI[lang] || [];
    if (!list.length) return;
    const i = Math.floor(Math.random() * list.length);
    setIndex(i);
    setShow(false);
  }

  const entry = OYUN_VERISI[lang]?.[index] || { gibberish: '', answer: '' };
  return (
    <div
      className="max-w-sm mx-auto mt-4 p-4 bg-white rounded shadow text-center"
      style={lang === 'HE' ? { direction: 'rtl' } : {}}
    >
      <div className="text-2xl font-bold mb-4">{entry.gibberish}</div>
      {show && <div className="text-xl mb-4 text-green-600">{entry.answer}</div>}
      <div className="space-x-2">
        <button className="bg-blue-500 text-white px-3 py-1 rounded m-1" onClick={() => setShow(true)}>
          {lang === 'HE' ? 'הצג תשובה' : 'Show Answer'}
        </button>
        <button className="bg-gray-600 text-white px-3 py-1 rounded m-1" onClick={newGame}>
          {lang === 'HE' ? 'משחק חדש' : 'New Game'}
        </button>
      </div>
    </div>
  );
}

// sample usage
const root = ReactDOM.createRoot(document.getElementById('root'));
root.render(<ShelterGame lang="HE" />);


