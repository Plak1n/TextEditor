import TextEditor as te
import unittest
from Fonts import view_colors,fonts

class TestCase(unittest.TestCase):
        
    def setUp(self) -> None:
        return super().setUp()
    
    
    def test_new_file(self):
        # Проверка на пустое текстовое поле при создание текстового файла
        self.assertTrue(te.new_file())
        self.assertEqual(te.new_file(),'\n')

    
    def test_fonts(self):
        # Проверка шрифтов на соответсвие
        self.assertIn('Arial',fonts['Arial']['font'])
        self.assertIn('Red Hat Mono',fonts['Red Hat']['font'])   
    
    
    def test_view_colors(self):
        # Проверка тем на соответсвие
        self.assertIn('dark',view_colors)
        self.assertIn('light',view_colors)  
    
    
    def test_file_name(self):
        #Проверка имени файла
        self.assertRegex(te.file_name,"Untitled")


    #@unittest.skip('Skipping')
    def test_something(self):
        self.assertTrue(te.combination('Увеличить шрифт'))    

    def test_change_language(self):
        # Изменение языка
        self.assertTrue(te.change_lang_keyboard())

if __name__ == "__main__":
    unittest.main()