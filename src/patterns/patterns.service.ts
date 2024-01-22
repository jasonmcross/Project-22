import { Injectable } from '@nestjs/common';
import { Prisma, patternGroup } from '@prisma/client';
import { DatabaseService } from 'src/database/database.service';

@Injectable()
export class PatternsService {
  constructor(private readonly databaseService: DatabaseService) {}
  
  async create(createPatternDto: Prisma.patternsCreateInput) {
    return this.databaseService.patterns.create({
      data: createPatternDto
    });
  }

  async findAll(group?: 'Behavioral' | 'Structural' | 'Creational') {
    return this.databaseService.patterns.findMany({
      where:{
        group,
      }
    });
    return this.databaseService.patterns.findMany
  }

  async findOne(name: string) {
    return this.databaseService.patterns.findUnique({
      where:{
        name,
      }
    })
  }

  async update(name: string, updatePatternDto: Prisma.patternsUpdateInput) {
    return this.databaseService.patterns.update({
      where:{
        name,
      },
      data: updatePatternDto
    })
  }

  async remove(name: string) {
    return this.databaseService.patterns.delete({
      where: {
        name,
      }
    });
  }
}
