import os, sys
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))
import pytest
from modules.data_manager import FAQStore
from modules.nlp import FAQEngine, preprocess

CSV = os.path.join(os.path.dirname(os.path.dirname(__file__)), "data", "faqs.csv")


@pytest.fixture()
def store(tmp_path):
    import shutil
    p = tmp_path / "faqs.csv"
    shutil.copy(CSV, p)
    s = FAQStore(p)
    assert s.load() == []
    return s


@pytest.fixture()
def engine(store):
    return FAQEngine(store.df)


def test_dataset_size(store):
    assert len(store.df) >= 40 and len(store.categories()) == 7


def test_exact_question(engine):
    r = engine.ask("How do I reset my password?")
    assert r.matched and r.question == "How do I reset my password?" and r.category == "Account and Registration"


def test_similar_wording(engine):
    assert engine.ask("I forgot my password, how can I change it?").question == "How do I reset my password?"
    assert engine.ask("how much does it cost?").category == "Pricing and Plans"
    assert engine.ask("Is my information safe and encrypted?").category == "Privacy and Security"
    assert engine.ask("can't sign in to my account").category == "Troubleshooting"


def test_uppercase(engine):
    assert engine.ask("HOW DO I RESET MY PASSWORD?").question == "How do I reset my password?"


def test_extra_spaces_and_punctuation(engine):
    assert engine.ask("   how   do  I   reset   my    password ???  ").question == "How do I reset my password?"


def test_unrelated_question(engine):
    r = engine.ask("What is the capital of France?")
    assert not r.matched and "could not find" in r.answer


def test_empty_input(engine):
    assert not engine.ask("").matched and not engine.ask("   ").matched and not engine.ask("???").matched


def test_threshold_is_configurable(engine):
    assert not engine.ask("password", threshold=0.95).matched


def test_related_questions(engine):
    assert len(engine.ask("How do I reset my password?").related) > 0


def test_kb_update_add_and_delete(store):
    q = "Can I bring my dog to the office?"
    assert not FAQEngine(store.df).ask(q).matched
    store.add("General Information", q, "Yes, dogs are welcome in our offices on Fridays.")
    assert FAQEngine(store.df).ask(q).matched
    reloaded = FAQStore(store.path); reloaded.load()
    assert q in reloaded.df["question"].values
    store.delete(q)
    assert not FAQEngine(store.df).ask(q).matched


def test_add_validation(store):
    for args in [("", "q", "a"), ("c", "", "a"), ("c", "q", "  ")]:
        with pytest.raises(ValueError):
            store.add(*args)
    with pytest.raises(ValueError):
        store.add("c", "what is novadesk?", "dup")


def test_missing_and_invalid_files(tmp_path):
    s = FAQStore(tmp_path / "nope.csv")
    assert "not found" in s.load()[0] and len(s.df) == 0
    assert not FAQEngine(s.df).ask("hello").matched
    bad = tmp_path / "bad.csv"
    bad.write_text("category,question,answer\nA,Q1,Ans\nB,,Ans\n,Q3,Ans\n")
    s2 = FAQStore(bad); w = s2.load()
    assert len(s2.df) == 1 and "invalid" in w[0]
    wrong = tmp_path / "wrong.csv"; wrong.write_text("a,b\n1,2\n")
    assert "columns" in FAQStore(wrong).load()[0]


def test_preprocess():
    assert preprocess("The  PRICES!!") == preprocess("price")
