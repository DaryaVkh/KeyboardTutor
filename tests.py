import unittest
from text_cleaner import TextCleaner


class MyTestCase(unittest.TestCase):
    def test_basic_trash(self):
        text_cleaner = TextCleaner("Hello ,        world !! ! \nhello,world ! ! !\nHELLo  ,         WORLD !")
        self.assertEqual("Hello, world! Hello, world! Hello, world!", text_cleaner.text)

    def test_punctuation(self):
        text_cleaner = TextCleaner("маМА МыЛА          \n     Раму... я,хочу.домоЙ.!?.")
        self.assertEqual("Мама мыла раму. Я, хочу. Домой.", text_cleaner.text)

    def test_word_wrapping(self):
        text_cleaner = TextCleaner("AW-\n      fUl    \n  tExT")
        self.assertEqual("Awful text", text_cleaner.text)

    def test_quotes(self):
        text_cleaner = TextCleaner("cAt saiD «MeoooooW»....???!!!;:,.")
        self.assertEqual('Cat said "meooooow".', text_cleaner.text)


if __name__ == '__main__':
    unittest.main()
