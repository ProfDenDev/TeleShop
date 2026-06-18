





# from pathlib import Path
#
# from openpyxl import load_workbook
#
# from app.services.importers.dto.product_import_dto import (
#     ProductImportDTO,
# )
#
#
# class XlsxImporter:
#     """
#     Импорт товаров из XLSX файла.
#     """
#
#     def __init__(self, file_path: str):
#         self.file_path = Path(file_path)
#
#     def import_products(
#         self,
#     ) -> list[ProductImportDTO]:
#
#         workbook = load_workbook(
#             self.file_path,
#             data_only=True,
#         )
#
#         sheet = workbook["Товары"]
#
#         products: list[
#             ProductImportDTO
#         ] = []
#
#         for row in sheet.iter_rows(
#             min_row=2,
#             values_only=True,
#         ):
#
#             sku = row[0]
#
#             if not sku:
#                 continue
#
#             product = ProductImportDTO(
#                 sku=str(row[0]).strip(),
#                 title=str(row[1]).strip(),
#                 description=row[2],
#                 category_slug=row[3],
#                 brand_name=row[4],
#                 price_uah=row[5],
#                 quantity=row[6] or 1,
#                 weight_g=row[7],
#                 dimensions=row[8],
#             )
#
#             products.append(product)
#
#         return products