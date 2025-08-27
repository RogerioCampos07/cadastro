from requests import get


class DataCompanyClient:
    def __init__(self):
        self.__base_url =  'https://brasilapi.com.br/api/cnpj/v1/'


    def get_data_company(self,cnpj):
        response = get(f'{self.__base_url}{cnpj}')
        dados = response.json()
        return dados
    
    def get_name_company(self,cnpj):
        company = self.get_data_company(cnpj)
        names = {}
        names['fantasy_name'] = company.get('nome_fantasia')
        names['social_name'] = company.get('razao_social')
        
        return names


    def address_company(self,cnpj):
        dados = {}
        company = self.get_data_company(cnpj)
        dados['type'] = company.get("descricao_tipo_de_logradouro")
        dados['street'] = company['logradouro']
        dados['address_number'] = company['numero']
        dados['community'] = company['bairro']
        dados['city'] = company.get('municipio')
        dados['uf'] = company.get('uf')
        dados['cep'] = company.get('cep')

        return dados
    
    
    
    
    