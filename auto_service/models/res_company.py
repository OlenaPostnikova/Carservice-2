# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

import base64
import io
import logging
import os
import re

from odoo import api, fields, models, tools, _, Command
from odoo.exceptions import ValidationError, UserError
from odoo.modules.module import get_resource_path
from odoo.tools import html2plaintext
from random import randrange
from PIL import Image

_logger = logging.getLogger(__name__)


class Company(models.Model):
    _name = "res.company"
    _inherit = 'res.company'

    mot_number = fields.Char(required=False, string='Mot ID')