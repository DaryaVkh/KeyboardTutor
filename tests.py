import unittest
from text_cleaner import TextCleaner


class MyTestCase(unittest.TestCase):
    def test_basic_trash(self):
        text = TextCleaner.clean_text('''Hello ,        world !! ! 
        hello,world ! ! !\nHELLo  ,         WORLD !''')
        self.assertEqual("Hello, world! Hello, world! Hello, world!",
                         text)

    def test_punctuation(self):
        text = TextCleaner.clean_text('''маМА МыЛА          
             Раму... я,хочу.домоЙ.!?.''')
        self.assertEqual("Мама мыла раму. Я, хочу. Домой.",
                         text)

    def test_word_wrapping(self):
        text = TextCleaner.clean_text("AW-\n      fUl    \n  tExT")
        self.assertEqual("Awful text", text)

    def test_quotes(self):
        text = TextCleaner.clean_text("cAt saiD «MeoooooW»....???!!!;:,.")
        self.assertEqual('Cat said "meooooow".', text)


if __name__ == '__main__':
    unittest.main()
