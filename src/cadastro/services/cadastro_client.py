import re
from typing import Optional
from requests import get, exceptions
from loguru import logger
from validate_cnpj import is_valid


logger.add('app.log', rotation="10 MB")




class DataCompanyClient:
    def __init__(self):
        self.__base_url = 'https://brasilapi.com.br/api/cnpj/v1/'
        

    def __validate_cnpj_and_clean_mask(self, cnpj: str) -> tuple[bool, str]:
        cnpj_cleaned = re.sub(r'\D', '', cnpj)
        cnpj_valid = is_valid(cnpj_cleaned)
        return cnpj_cleaned,cnpj_valid

    def get_data_company(self, cnpj: str) -> Optional[dict]:
        cnpj_cleaned,cnpj_valid = self.__validate_cnpj_and_clean_mask(cnpj)
        if not cnpj_valid:
            logger.warning(f'CNPJ inválido: {cnpj}')
            return None

        try:
            response = get(f'{self.__base_url}{cnpj_cleaned}', timeout=10)
            response.raise_for_status()
            data = response.json()
            
            return data

        except exceptions.Timeout:
            logger.error(f'Timeout ao buscar dados do CNPJ {cnpj_cleaned}')
        except exceptions.HTTPError as e:
            status = e.response.status_code if e.response else "unknown"
            logger.error(f'Erro HTTP ao buscar {cnpj_cleaned}: {e} - Status: {status}')
        except exceptions.RequestException as e:
            logger.error(f'Erro de conexão ao buscar {cnpj_cleaned}: {e}')
        except ValueError:
            logger.error(f'Erro ao decodificar JSON para {cnpj_cleaned}: {response.text}')
        except Exception as e:
            logger.exception(f'Erro inesperado ao buscar dados para {cnpj_cleaned}: {e}')

        return None

    def get_name_company(self, cnpj: str) -> Optional[dict]:
        company = self.get_data_company(cnpj)
        if not company:
            return None
        return {
            'fantasy_name': company.get('nome_fantasia'),
            'social_name': company.get('razao_social'),
        }

    def address_company(self, cnpj: str) -> Optional[dict]:
        company = self.get_data_company(cnpj)
        if not company:
            return None
        return {
            'type': company.get('descricao_tipo_de_logradouro'),
            'street': company.get('logradouro'),
            'address_number': company.get('numero'),
            'community': company.get('bairro'),
            'city': company.get('municipio'),
            'uf': company.get('uf'),
            'cep': company.get('cep'),
        }
