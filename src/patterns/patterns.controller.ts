import { Controller, Get, Post, Body, Patch, Param, Delete, Query } from '@nestjs/common';
import { PatternsService } from './patterns.service';
import { Prisma } from '@prisma/client';
import { query } from 'express';

@Controller('patterns')
export class PatternsController {
  constructor(private readonly patternsService: PatternsService) {}

  @Post()
  create(@Body() createPatternDto: Prisma.patternsCreateInput) {
    return this.patternsService.create(createPatternDto);
  }

  @Get()
  findAll(@Query('group') group?: 'Behavioral' | 'Structural' | 'Creational') {
    return this.patternsService.findAll();
  }

  @Get(':name')
  findOne(@Param('name') name: string) {
    return this.patternsService.findOne(name);
  }

  @Patch(':name')
  update(@Param('id') name: string, @Body() updatePatternDto: Prisma.patternsUpdateInput) {
    return this.patternsService.update(name, updatePatternDto);
  }

  @Delete(':name')
  remove(@Param('name') name: string) {
    return this.patternsService.remove(name);
  }
}
