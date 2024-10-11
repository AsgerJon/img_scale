"""ImgTool encapsulates image editing in a class. """
#  AGPL-3.0 license
#  Copyright (c) 2024 Asger Jon Vistisen
from __future__ import annotations

from PIL.Image import Image
from PIL.Image import open as imgOpen
from worktoy.base import BaseObject, overload
from worktoy.desc import AttriBox, Field


class ImgTool(BaseObject):
  """ImgTool encapsulates image editing in a class. """

  sourceFile = AttriBox[str]()
  targetFile = AttriBox[str]()

  sourceImage = AttriBox[Image]()
  tempImage = AttriBox[Image]()

  aspect = Field()

  @overload(str)
  def load(self, filePath: str) -> None:
    """Load image from file."""
    self.sourceFile = filePath
    return self.load()

  @overload()
  def load(self) -> None:
    """Load image from the source file."""
    with imgOpen(self.sourceFile) as img:
      self.sourceImage = img.copy()
      self.tempImage = img.copy()

  def saveAs(self, filePath: str) -> None:
    """Save image as"""
    self.targetFile = filePath
    self.save()

  @overload(str)
  def save(self, filePath: str) -> None:
    """Save the image to a file."""
    self.saveAs(filePath)

  @overload()
  def save(self) -> None:
    """Save the image to the target file."""
    Image.save(self.tempImage, self.targetFile, format='PNG')

  @overload(int, int)
  def resize(self, width: int, height: int, ) -> None:
    """Resize the image."""
    if width < 0:
      return self.resize(height * self.aspect, height, )
    if height < 0:
      return self.resize(width, width / self.aspect, )
    self.tempImage = Image.resize(self.sourceImage, (width, height))

  @aspect.GET
  def _getAspect(self, ) -> float:
    """Get the aspect ratio of the image."""
    return self.sourceImage.width / self.sourceImage.height
