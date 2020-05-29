from zope.interface import implementer
from sqlalchemy import (
    Column,
    Unicode,
    Integer,
    ForeignKey,
    UniqueConstraint,
)
from sqlalchemy.orm import relationship, backref, joinedload
from sqlalchemy.ext.declarative import declared_attr

from clld.db.meta import Base, PolymorphicBaseMixin
from clld.db.models.common import Language, IdNameDescriptionMixin

from clld_phylogeny_plugin.interfaces import IPhylogeny


@implementer(IPhylogeny)
class Phylogeny(Base, PolymorphicBaseMixin, IdNameDescriptionMixin):
    """
    A Phylogeny represents an evolutionary tree that may be used to map Parameters onto.
    """
    newick = Column(Unicode)

    @staticmethod
    def refine_factory_query(query):
        return query.options(
            joinedload(Phylogeny.treelabels)
            .joinedload(TreeLabel.language_assocs)
            .joinedload(LanguageTreeLabel.language))


class TreeLabel(Base, IdNameDescriptionMixin):
    """
    A Label used for a leaf node in a Phylogeny.
    """
    phylogeny_pk = Column(Integer, ForeignKey('phylogeny.pk'))

    @declared_attr
    def phylogeny(cls):
        return relationship(Phylogeny, backref=backref('treelabels', order_by=[cls.pk]))

    @property
    def languages(self):
        return [la.language for la in sorted(self.language_assocs, key=lambda la: la.ord)]


class LanguageTreeLabel(Base):
    """
    A TreeLabel may be mapped to multiple Language objects. This many-to-many relationship
    is mediated through LanguageTreeLabel.
    """
    __table_args__ = (UniqueConstraint('language_pk', 'treelabel_pk'),)

    language_pk = Column(Integer, ForeignKey('language.pk'), nullable=False)
    language = relationship(Language)
    treelabel_pk = Column(Integer, ForeignKey('treelabel.pk'), nullable=False)
    treelabel = relationship(TreeLabel, backref='language_assocs')
    ord = Column(Integer, default=1)
