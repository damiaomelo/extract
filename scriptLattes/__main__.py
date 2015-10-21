#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
scriptlattes.__main__
~~~~~~~~~~~~~~~~~~~~~

The main entry point for the command line interface.

Invoke as ``scriptlattes`` (if installed)
or ``python -m scriptlattes`` (no install required).
"""
from __future__ import absolute_import, unicode_literals
import logging
import sys

from configobj import ConfigObj
from pathlib import Path
from cache import cache

from grupo import Grupo
from scriptLattes.log import configure_stream
from util import criarDiretorio, copiarArquivos
from validate import Validator

logger = logging.getLogger(__name__)

# FIXME: incluir comentários abaixo (retirar dos exemplos)
# FIXME: implementar opção de gravar arquivo de configuração padrão
# FIXME: resolver caminhos da configuração relativamente ao caminho do arquivo de config, caso a config não seja um caminho absoluto

default_configuration = u"""
global-nome_do_grupo = string
global-arquivo_de_entrada = string
global-diretorio_de_saida = string
global-email_do_admin = string
global-idioma = string(default='PT')
global-itens_desde_o_ano = integer(min=1990)
global-itens_ate_o_ano = integer
global-itens_por_pagina = integer(min='1', default='1000')
global-criar_paginas_jsp = boolean(default='não')
global-google_analytics_key = string
global-prefixo = string
global-diretorio_de_armazenamento_de_cvs = string
global-diretorio_de_armazenamento_de_doi = string
global-salvar_informacoes_em_formato_xml = boolean(default='não')

global-identificar_publicacoes_com_qualis = boolean(default='não')
global-usar_cache_qualis = boolean(default='sim')
global-arquivo_areas_qualis = string
global-arquivo_qualis_de_congressos = string
global-arquivo_qualis_de_periodicos = string

relatorio-salvar_publicacoes_em_formato_ris = boolean(default='não')
relatorio-incluir_artigo_em_periodico = boolean(default='sim')
relatorio-incluir_livro_publicado = boolean(default='sim')
relatorio-incluir_capitulo_de_livro_publicado = boolean(default='sim')
relatorio-incluir_texto_em_jornal_de_noticia = boolean(default='sim')
relatorio-incluir_trabalho_completo_em_congresso = boolean(default='sim')
relatorio-incluir_resumo_expandido_em_congresso = boolean(default='sim')
relatorio-incluir_resumo_em_congresso = boolean(default='sim')
relatorio-incluir_artigo_aceito_para_publicacao = boolean(default='sim')
relatorio-incluir_apresentacao_de_trabalho = boolean(default='sim')
relatorio-incluir_outro_tipo_de_producao_bibliografica = boolean(default='sim')

relatorio-incluir_software_com_patente = boolean(default='sim')
relatorio-incluir_software_sem_patente = boolean(default='sim')
relatorio-incluir_produto_tecnologico = boolean(default='sim')
relatorio-incluir_processo_ou_tecnica = boolean(default='sim')
relatorio-incluir_trabalho_tecnico = boolean(default='sim')
relatorio-incluir_outro_tipo_de_producao_tecnica = boolean(default='sim')

relatorio-incluir_patente = boolean(default='sim')
relatorio-incluir_programa_computador = boolean(default='sim')
relatorio-incluir_desenho_industrial = boolean(default='sim')

relatorio-incluir_producao_artistica = boolean(default='sim')

relatorio-mostrar_orientacoes = boolean(default='sim')
relatorio-incluir_orientacao_em_andamento_pos_doutorado = boolean(default='sim')
relatorio-incluir_orientacao_em_andamento_doutorado = boolean(default='sim')
relatorio-incluir_orientacao_em_andamento_mestrado = boolean(default='sim')
relatorio-incluir_orientacao_em_andamento_monografia_de_especializacao = boolean(default='sim')
relatorio-incluir_orientacao_em_andamento_tcc = boolean(default='sim')
relatorio-incluir_orientacao_em_andamento_iniciacao_cientifica = boolean(default='sim')
relatorio-incluir_orientacao_em_andamento_outro_tipo = boolean(default='sim')

relatorio-incluir_orientacao_concluida_pos_doutorado = boolean(default='sim')
relatorio-incluir_orientacao_concluida_doutorado = boolean(default='sim')
relatorio-incluir_orientacao_concluida_mestrado = boolean(default='sim')
relatorio-incluir_orientacao_concluida_monografia_de_especializacao = boolean(default='sim')
relatorio-incluir_orientacao_concluida_tcc = boolean(default='sim')
relatorio-incluir_orientacao_concluida_iniciacao_cientifica = boolean(default='sim')
relatorio-incluir_orientacao_concluida_outro_tipo = boolean(default='sim')

relatorio-incluir_projeto = boolean(default='sim')
relatorio-incluir_premio = boolean(default='sim')
relatorio-incluir_participacao_em_evento = boolean(default='sim')
relatorio-incluir_organizacao_de_evento = boolean(default='sim')
relatorio-incluir_internacionalizacao = boolean(default='não')

grafo-mostrar_grafo_de_colaboracoes = boolean(default='sim')
grafo-mostrar_todos_os_nos_do_grafo = boolean(default='sim')
grafo-considerar_rotulos_dos_membros_do_grupo = boolean(default='sim')
grafo-mostrar_aresta_proporcional_ao_numero_de_colaboracoes = boolean(default='sim')

grafo-incluir_artigo_em_periodico = boolean(default='sim')
grafo-incluir_livro_publicado = boolean(default='sim')
grafo-incluir_capitulo_de_livro_publicado = boolean(default='sim')
grafo-incluir_texto_em_jornal_de_noticia = boolean(default='sim')
grafo-incluir_trabalho_completo_em_congresso = boolean(default='sim')
grafo-incluir_resumo_expandido_em_congresso = boolean(default='sim')
grafo-incluir_resumo_em_congresso = boolean(default='sim')
grafo-incluir_artigo_aceito_para_publicacao = boolean(default='sim')
grafo-incluir_apresentacao_de_trabalho = boolean(default='sim')
grafo-incluir_outro_tipo_de_producao_bibliografica = boolean(default='sim')

grafo-incluir_software_com_patente = boolean(default='sim')
grafo-incluir_software_sem_patente = boolean(default='sim')
grafo-incluir_produto_tecnologico = boolean(default='sim')
grafo-incluir_processo_ou_tecnica = boolean(default='sim')
grafo-incluir_trabalho_tecnico = boolean(default='sim')
grafo-incluir_outro_tipo_de_producao_tecnica = boolean(default='sim')

grafo-incluir_patente = boolean(default='sim')
grafo-incluir_programa_computador = boolean(default='sim')
grafo-incluir_desenho_industrial = boolean(default='sim')

grafo-incluir_producao_artistica = boolean(default='sim')
grafo-incluir_grau_de_colaboracao = boolean(default='não')

mapa-mostrar_mapa_de_geolocalizacao = boolean(default='sim')
mapa-incluir_membros_do_grupo = boolean(default='sim')
mapa-incluir_alunos_de_pos_doutorado = boolean(default='sim')
mapa-incluir_alunos_de_doutorado = boolean(default='sim')
mapa-incluir_alunos_de_mestrado = boolean(default='não')
"""


def load_config(filename):
    spec = default_configuration.split("\n")
    config = ConfigObj(infile=filename, configspec=spec, file_error=False)
    validator = Validator()
    res = config.validate(validator, copy=True)
    return config


def cli():
    """Add some useful functionality here or import from a submodule."""
    # configure root logger to print to STDERR
    configure_stream(level='DEBUG')

    # launch the command line interface
    logger.info("Executando '{}'".format(' '.join(sys.argv)))

    # FIXME: use docopt for command line arguments (or argparse)
    config_filename = sys.argv[1]
    if not Path(config_filename).exists():
        logger.error("Arquivo de configuração '{}' não existe.".format(config_filename))
        return -1
    config = load_config(config_filename)

    # configure cache
    if 'global-diretorio_de_armazenamento_de_cvs' in config and config.get('global-diretorio_de_armazenamento_de_cvs'):
        cache.set_directory(config['global-diretorio_de_armazenamento_de_cvs'])

    ids_file_path = Path(config['global-arquivo_de_entrada'])
    if not ids_file_path.exists():
        # Path(sys.argv[1]).parent / ids_filename
        ids_file_path = Path(sys.argv[1]).with_name(ids_file_path.name)
        if not ids_file_path.exists():
            logger.error("Arquivo de lista de IDs não existe: '{}'".format(ids_file_path))
            return -1
    if not ids_file_path.is_file():
        logger.error("Caminho para arquivo da lista de IDs '{}' não é um arquivo".format(ids_file_path))
        return -1
    ids_file_path = ids_file_path.resolve()

    group = Grupo(ids_file_path=ids_file_path,
                  desde_ano=config['global-itens_desde_o_ano'],
                  ate_ano=config['global-itens_ate_o_ano'])
    # group.imprimirListaDeParametros()
    group.imprimirListaDeRotulos()

    # if criarDiretorio('global-diretorio_de_saida')):
    if 'global-diretorio_de_saida' in config:
        group.carregarDadosCVLattes()  # obrigatorio
        group.compilarListasDeItems()  # obrigatorio
        group.identificarQualisEmPublicacoes()  # obrigatorio
        group.calcularInternacionalizacao()  # obrigatorio
        # group.imprimirMatrizesDeFrequencia()

        group.gerarGrafosDeColaboracoes()  # obrigatorio
        # group.gerarGraficosDeBarras() # java charts
        group.gerarMapaDeGeolocalizacao()  # obrigatorio
        group.gerarPaginasWeb()  # obrigatorio
        group.gerarArquivosTemporarios()  # obrigatorio

        # copiar images e css
        copiarArquivos(group.obterParametro('global-diretorio_de_saida'))

        # finalizando o processo
        print('\n\n\n[PARA REFERENCIAR/CITAR ESTE SOFTWARE USE]')
        print('    Jesus P. Mena-Chalco & Roberto M. Cesar-Jr.')
        print('    scriptLattes: An open-source knowledge extraction system from the Lattes Platform.')
        print('    Journal of the Brazilian Computer Society, vol.15, n.4, páginas 31-39, 2009.')
        print('    http://dx.doi.org/10.1007/BF03194511')
        print('\n\nscriptLattes executado!')

        # return 0


if __name__ == '__main__':
    # exit using whatever exit code the CLI returned
    sys.exit(cli())