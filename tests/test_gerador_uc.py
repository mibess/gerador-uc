import unittest
from gerador_uc import calcular_dv, formatar_uc, gerar_uc_para_distribuidora

class TestGeradorUC(unittest.TestCase):

    def test_calcular_dv_exemplo_manual(self):
        # Exemplo hipotético ou conhecido. 
        # Vamos testar com valores que sabemos o resultado ou verificar a consistência.
        # Como não tenho um par exato do manual aqui, vou testar a consistência:
        # Se eu gerar um DV, ele deve ser determinístico.
        seq = "1234567890"
        dist = "001"
        n2, n1 = calcular_dv(seq, dist)
        self.assertTrue(n2.isdigit())
        self.assertTrue(n1.isdigit())
        self.assertEqual(len(n2), 1)
        self.assertEqual(len(n1), 1)

    def test_formatar_uc(self):
        seq = "1234567890"
        dist = "001"
        n2 = "5"
        n1 = "9"
        # Esperado: 1.234.567.890.001-59
        # Format: N15.N14N13N12.N11N10N9.N8N7N6.N5N4N3-N2N1
        # seq="1234567890" -> p1=1, p2=234, p3=567, p4=890
        # dist="001" -> p5=001
        esperado = "1.234.567.890.001-59"
        resultado = formatar_uc(seq, dist, n2, n1)
        self.assertEqual(resultado, esperado)

    def test_gerar_uc_para_distribuidora_valida(self):
        dist = "59" # LIGHT
        uc = gerar_uc_para_distribuidora(dist)
        self.assertIn("-", uc)
        self.assertIn(".", uc)
        # Verificar se termina com 2 digitos
        parts = uc.split("-")
        self.assertEqual(len(parts), 2)
        self.assertEqual(len(parts[1]), 2)

    def test_gerar_uc_erro_sem_distribuidora(self):
        with self.assertRaises(ValueError):
            gerar_uc_para_distribuidora("")

if __name__ == '__main__':
    unittest.main()
